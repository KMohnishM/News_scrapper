# News Digest Web App

A world-class, visually stunning news digest application with a robust Django backend and a modern Next.js frontend. The backend fetches, deduplicates, and summarizes news articles by category using NewsData.io and OpenRouter's DeepSeek model. The frontend displays these summaries in a premium, black-themed, glassmorphic UI.

---

## Table of Contents
- [Features](#features)
- [Tech Stack & Tools](#tech-stack--tools)
- [Backend Setup (Django)](#backend-setup-django)
- [Frontend Setup (Next.js)](#frontend-setup-nextjs)
- [API Endpoints](#api-endpoints)
- [Data Models](#data-models)
- [Background Tasks & Deduplication](#background-tasks--deduplication)
- [Celery Commands](#celery-commands)
- [Environment Variables](#environment-variables)
- [Deployment](#deployment)
- [Frontend Structure](#frontend-structure)
- [Development & Debugging](#development--debugging)
- [Troubleshooting](#troubleshooting)
- [Credits](#credits)

---

## Features

### Backend (Django)
- **News Fetching:** Uses NewsData.io's `/latest` endpoint to fetch the latest news by category.
- **Summarization:** Summarizes articles using OpenRouter's DeepSeek model via HTTP API.
- **Deduplication:** Deduplicates articles daily using URL hashing and Redis cache.
- **Categorization:** Maps and groups articles into categories (`top`, `sports`, `technology`).
- **Multiple API Endpoints:** Exposes endpoints for digests, fresh digests, articles, and categorized sections.
- **Robust Error Handling:** Handles API errors, missing data, and ensures fresh content on every request.
- **User Preferences:** (Model present) Can be extended for personalized digests.

### Frontend (Next.js)
- **Modern UI:** Black-themed, glassmorphic, premium look inspired by The Verge, BBC, NYT, and Apple News.
- **Responsive Design:** Fully mobile-friendly and visually cohesive.
- **Dynamic News Cards:** Renders each category as a glassy card with colored accent bars and colored links.
- **Neon Branding:** Glassy, fixed header with neon app name and navigation.
- **Dark Mode:** All backgrounds, cards, and text are styled for dark mode.
- **API Integration:** Fetches and displays categorized summaries from the backend API.
- **Error Handling:** Graceful loading and error states.

---

## Tech Stack & Tools

- **Backend:** Python 3, Django 5, Celery (for async tasks), Redis (for caching/deduplication)
- **Frontend:** Next.js 14, React 18, Tailwind CSS, modern CSS (glassmorphism, gradients)
- **APIs:**
  - [NewsData.io](https://newsdata.io/) – News data provider
  - [OpenRouter (DeepSeek)](https://openrouter.ai/) – Summarization model
- **Other Tools:** Gunicorn (production WSGI), Nginx (reverse proxy), Vercel (optional frontend hosting), Docker (optional for deployment)

---

## Backend Setup (Django)

1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/news-digest-app.git
   cd news-digest-app/backend
   ```

2. **Create and activate a virtual environment:**
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   - Copy `.env.example` to `.env` and fill in your API keys:
     ```env
     NEWSDATA_API_KEY=your_newsdata_api_key
     OPENROUTER_API_KEY=your_openrouter_api_key
     REDIS_URL=redis://localhost:6379/0
     DJANGO_SECRET_KEY=your_secret_key
     DJANGO_DEBUG=False
     ALLOWED_HOSTS=localhost,127.0.0.1
     ```

5. **Run migrations:**
   ```sh
   python manage.py migrate
   ```

6. **Collect static files:**
   ```sh
   python manage.py collectstatic
   ```

7. **Start the backend server:**
   ```sh
   python manage.py runserver
   ```

8. **(Optional) Create a superuser for Django admin:**
   ```sh
   python manage.py createsuperuser
   ```

9. **(Optional) Start Celery worker and beat for background tasks:**
   See [Celery Commands](#celery-commands).

---

## API Endpoints

All API endpoints are under `/api/`:

| Endpoint                      | Method | Description                                                                 |
|-------------------------------|--------|-----------------------------------------------------------------------------|
| `/api/digests/`               | GET    | List all digests (summaries of news for each day).                          |
| `/api/digests/fresh/`         | GET    | Generate and return a fresh digest (fetches new news, summarizes, saves).   |
| `/api/digests/sections/`      | GET    | Returns categorized, HTML-formatted summaries for the frontend.             |
| `/api/articles/`              | GET    | List all news articles in the database.                                     |

### Example: `/api/digests/sections/` Response
```json
[
  {
    "category": "Top",
    "paragraph": "<a href='https://news.link/1'>Headline 1</a> ... <a href='https://news.link/2'>Headline 2</a> ..."
  },
  {
    "category": "Sports",
    "paragraph": "<a href='https://news.link/3'>Headline 3</a> ..."
  }
]
```

#### **Authentication**
- All endpoints are public by default. For production, consider adding authentication for admin or user-specific endpoints.

#### **Error Handling**
- All endpoints return standard HTTP status codes and error messages for invalid requests or server errors.

---

## Data Models

### NewsArticle
- `title`: CharField, max 300
- `url`: URLField
- `content`: TextField
- `published_at`: DateTimeField
- `category`: CharField (choices: international, indian, sports, tech)
- `source`: CharField

### Digest
- `date`: DateField (auto_now_add)
- `summary`: TextField (HTML-formatted digest)
- `articles`: ManyToManyField to NewsArticle

### UserPreferences
- `user`: OneToOneField to User
- `preferred_categories`: CharField (comma-separated)

---

## Background Tasks & Deduplication

- **Celery Tasks:**  
  - `fetch_and_summarize_news`: Fetches news, summarizes, and creates a digest.
  - `create_news_and_summaries`: Core logic for fetching, deduplication, summarization, and saving.
  - `build_digest`: Used for the `/sections/` endpoint, returns categorized summaries.

- **Deduplication:**  
  - Uses Redis cache to store a hash of each article URL for 24 hours.
  - Functions: `is_article_seen(url)`, `mark_article_seen(url)`

- **Summarization:**
  - Uses OpenRouter's DeepSeek model via HTTP POST to generate concise summaries for each article.
  - Handles API errors and rate limits with retries and fallbacks.

---

## Celery Commands

To enable background and scheduled tasks, run both of these commands (in separate terminals or as background services):

| Command                                 | Purpose                |
|------------------------------------------|------------------------|
| `celery -A newsdigest worker -l info`    | Run Celery worker      |
| `celery -A newsdigest beat -l info`      | Run Celery scheduler   |

- The **worker** processes background jobs (like summarization).
- The **beat** scheduler triggers periodic tasks (like fetching news every X minutes).

**Tip:** Use a process manager like `supervisord` or `systemd` to keep these running in production.

---

## Frontend Setup (Next.js)

1. **Navigate to the frontend directory:**
   ```sh
   cd ../frontend
   ```

2. **Install dependencies:**
   ```sh
   npm install
   ```

3. **Set up environment variables:**
   - Copy `.env.example` to `.env.local` and set your backend API URL:
     ```env
     NEXT_PUBLIC_API_URL=http://localhost:8000/api/digests/sections/
     ```

4. **Start the development server:**
   ```sh
   npm run dev
   ```

5. **Build for production:**
   ```sh
   npm run build
   npm run start
   ```

---

## Frontend Structure

- **`src/app/page.js`**: Main page, renders the news digest.
- **`src/components/NewsDigest.js`**: Fetches `/api/digests/sections/` and renders each section as a glassy card.
- **`src/components/Header.js`**: Glassmorphic, fixed header with neon branding.
- **`src/components/Footer.js`**: Minimal, glassy footer.
- **`src/components/CategorySection.js`**: (If present) Renders a single news category.
- **`src/components/ThemeToggle.js`**: (If present) Allows toggling dark/light mode (default is black theme).
- **`src/app/globals.css`**: Global styles, including black theme, glassmorphism, and font imports.

---

## Environment Variables

### **Backend**
- `NEWSDATA_API_KEY` – Your NewsData.io API key
- `OPENROUTER_API_KEY` – Your OpenRouter API key
- `REDIS_URL` – Redis connection string
- `DJANGO_SECRET_KEY` – Django secret key
- `DJANGO_DEBUG` – Set to `False` in production
- `ALLOWED_HOSTS` – Comma-separated list of allowed hosts

### **Frontend**
- `NEXT_PUBLIC_API_URL` – URL of your backend API endpoint

---

## Deployment

### **Frontend**
- Deploy to [Vercel](https://vercel.com/) for best Next.js support.
- Or use any Node.js host (Netlify, DigitalOcean, AWS, etc.).
- For static export: `npm run export` and deploy the `out/` directory.

### **Backend**
- Deploy to [Render](https://render.com/), [DigitalOcean](https://www.digitalocean.com/), AWS, or any server with Python support.
- Use Gunicorn or uWSGI as the WSGI server.
- Use Nginx or Caddy as a reverse proxy for HTTPS and static files.

### **Reverse Proxy Example (Nginx)**
```nginx
server {
    server_name yourdomain.com;

    location /api/ {
        proxy_pass http://127.0.0.1:8000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## Development & Debugging

- **Hot reload**: Both Django and Next.js support hot reloading in development.
- **Logs**: Check backend logs for API errors and frontend console for UI issues.
- **Testing**: Add Django tests in `backend/digest/tests.py` and React tests in `frontend/src/__tests__/`.
- **Linting:** Use `eslint` for frontend and `flake8` or `black` for backend code quality.
- **Admin Panel:** Access Django admin at `/admin/` for managing articles, digests, and users.

---

## Troubleshooting

- **API Key Issues:**
  - Ensure your NewsData.io and OpenRouter API keys are valid and not rate-limited.
  - Check `.env` files and environment variable setup.

- **CORS Errors:**
  - Make sure Django CORS headers are configured if frontend and backend are on different domains.

- **Celery/Redis Issues:**
  - Ensure Redis is running and accessible at the configured `REDIS_URL`.
  - Check Celery logs for task errors.

- **Build/Static Issues:**
  - Run `python manage.py collectstatic` after changes to static files.
  - For Next.js, rebuild with `npm run build` if you change config or environment variables.

- **Port Conflicts:**
  - Default ports: Django (8000), Next.js (3000). Change if needed.

---

## Credits

- **NewsData.io** – News data provider
- **OpenRouter (DeepSeek)** – Summarization model
- **UI Inspiration** – The Verge, BBC, NYT, Apple News
- **Tech** – Django, Next.js, Tailwind CSS, Redis, Celery

---

**For questions or contributions, open an issue or pull request!** 