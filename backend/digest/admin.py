from django.contrib import admin
from .models import NewsArticle, Digest, UserPreferences

class NewsArticleInline(admin.TabularInline):
    model = Digest.articles.through
    extra = 1

class DigestAdmin(admin.ModelAdmin):
    inlines = [NewsArticleInline]
    list_display = ('date',)
    filter_horizontal = ('articles',)

# Register your models here.
admin.site.register(NewsArticle)
admin.site.register(Digest, DigestAdmin)
admin.site.register(UserPreferences)
