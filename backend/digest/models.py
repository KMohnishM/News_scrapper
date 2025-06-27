from django.db import models
from django.contrib.auth.models import User

class NewsArticle(models.Model):
    CATEGORY_CHOICES = [
        ('international', 'International'),
        ('indian', 'Indian'),
        ('sports', 'Sports'),
        ('tech', 'Tech'),
    ]
    title = models.CharField(max_length=300)
    url = models.URLField()
    content = models.TextField()
    published_at = models.DateTimeField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    source = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class Digest(models.Model):
    date = models.DateField(auto_now_add=True)
    summary = models.TextField()
    articles = models.ManyToManyField(NewsArticle)

    def __str__(self):
        return f"Digest for {self.date}"

class UserPreferences(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    preferred_categories = models.CharField(max_length=100, help_text="Comma-separated categories")

    def __str__(self):
        return f"Preferences for {self.user.username}"
