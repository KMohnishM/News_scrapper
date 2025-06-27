from celery import shared_task
from .models import NewsArticle, Digest
import requests
from django.utils import timezone
from django.conf import settings
import logging
import time
from collections import defaultdict
import random
from datetime import datetime
from .utils import is_article_seen, mark_article_seen

logger = logging.getLogger(__name__)

OPENROUTER_API_KEY = getattr(settings, 'OPENROUTER_API_KEY', 'YOUR_OPENROUTER_API_KEY')
OPENROUTER_URL = 'https://openrouter.ai/api/v1/chat/completions'
DEEPSEEK_MODEL = 'deepseek/deepseek-r1-0528-qwen3-8b:free'

# Map your categories to GNews topics
CATEGORIES = {
    'international': 'world',
    'indian': 'nation',
    'sports': 'sports',
    'tech': 'technology',
}

CATEGORY_MAP = {
    "international": "top",
    "indian": "top",
    "sports": "sports",
    "tech": "technology",
}

def fetch_news(category):
    mapped_category = CATEGORY_MAP.get(category, category)
    url = "https://newsdata.io/api/1/latest"
    params = {
        "apikey": getattr(settings, 'NEWSDATA_API_KEY', 'YOUR_NEWSDATA_API_KEY'),
        "category": mapped_category,
        "language": "en",
        "country": "in" if category == "indian" else None,
    }
    resp = requests.get(url, params={k: v for k, v in params.items() if v})
    resp.raise_for_status()
    return resp.json().get("results", [])

def summarize_article(article):
    headers = {
        'Authorization': f'Bearer {OPENROUTER_API_KEY}',
        'Content-Type': 'application/json',
    }
    prompt = (
        "Summarize the following news article in one concise, informative sentence. "
        "Do not add extra commentary.\n\n"
        f"Headline: {article.get('title')}\n"
        f"Snippet: {article.get('description')}\n"
        f"Body: {article.get('full_content') or article.get('content') or ''}"
    )
    data = {
        "model": DEEPSEEK_MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that summarizes news articles."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 60,
        "temperature": 0.7,
    }
    try:
        resp = requests.post(OPENROUTER_URL, headers=headers, json=data, timeout=30)
        resp.raise_for_status()
        result = resp.json()
        summary = result['choices'][0]['message']['content'].strip()
        return summary
    except Exception as e:
        logger.error(f"OpenRouter summarization error: {e}")
        return article.get('title', 'No summary available.')

def create_news_and_summaries():
    today = timezone.now().date()
    all_category_sentences = {}
    for category in CATEGORIES:
        country = 'in' if category == 'indian' else 'us'
        articles = fetch_news(category)
        sentences = []
        for art in articles:
            url = art.get("link") or art.get("url")
            if not url or is_article_seen(url):
                continue
            try:
                summary = summarize_article(art)
            except Exception as e:
                logger.error(f"Summarization failed for {url}: {e}")
                continue
            mark_article_seen(url)
            news = NewsArticle.objects.create(
                title=art.get('title', '')[:300],
                url=url,
                content=art.get('full_content', '') or art.get('content', '') or art.get('description', ''),
                published_at=timezone.now(),  # Always use now
                category=category,
                source=art.get('source', {}).get('name', ''),
            )
            logger.info(f"Created article: {news.title} | published_at: {news.published_at} | url: {news.url}")
            sentence = f'<a href="{news.url}" target="_blank">{summary or news.title}</a>'
            sentences.append(sentence)
            time.sleep(3)  # Wait 3 seconds between LLM calls to avoid rate limit
        all_category_sentences[category] = sentences
        logger.info(f"Category {category} sentences: {sentences}")
    # Create digest paragraphs
    digest_paragraphs = []
    for category, sentences in all_category_sentences.items():
        if sentences:
            paragraph = f"<b>{CATEGORY_MAP[category]} News:</b> " + ' '.join(sentences)
            digest_paragraphs.append(paragraph)
    digest_text = '<br><br>'.join(digest_paragraphs)
    logger.info(f"Final digest_text: {digest_text}")
    # Fallback: if digest_text is empty, use article titles/links
    if not digest_text:
        logger.warning("Digest summary is empty, using fallback summary.")
        articles_today = NewsArticle.objects.filter(published_at__date=today)
        # Group by category
        cat_map = defaultdict(list)
        for a in articles_today:
            cat_map[a.category].append(f'<a href="{a.url}" target="_blank">{a.title}</a>')
        fallback_paragraphs = []
        for cat, links in cat_map.items():
            if links:
                paragraph = f"<b>{CATEGORY_MAP[cat].capitalize()} News:</b> " + ' '.join(links)
                fallback_paragraphs.append(paragraph)
        digest_text = '<br><br>'.join(fallback_paragraphs) or 'No summary available.'
    # After digest_text is built, add a timestamp for uniqueness
    digest_text += f'<br><br><i>Digest generated at {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</i>'
    digest = Digest.objects.create(summary=digest_text)
    # Attach all today's articles
    articles_today = NewsArticle.objects.filter(published_at__date=today)
    logger.info(f"Associating {articles_today.count()} articles with digest {digest.id} for date {today}")
    digest.articles.set(articles_today)
    return digest

@shared_task
def fetch_and_summarize_news():
    digest = create_news_and_summaries()
    return {
        'digest_id': digest.id,
        'digest_date': str(digest.date),
        'status': 'success',
    }

def build_digest():
    digest = []
    for cat_key, cat_label in CATEGORY_MAP.items():
        articles = fetch_news(cat_key)
        summaries = []
        for art in articles:
            url = art.get("link") or art.get("url")
            if not url or is_article_seen(url):
                continue
            try:
                summary = summarize_article(art)
            except Exception as e:
                logger.error(f"Summarization failed for {url}: {e}")
                continue
            mark_article_seen(url)
            summaries.append(f"<a href='{url}' target='_blank'>{summary}</a>")
        if summaries:
            paragraph = " ".join(summaries)
            digest.append({"category": cat_label, "paragraph": paragraph})
    return digest 