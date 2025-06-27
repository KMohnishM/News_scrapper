from django.urls import path
from .views import DigestListView, NewsArticleListView, FreshDigestView, FreshDigestSectionsView

urlpatterns = [
    path('digests/', DigestListView.as_view(), name='digest-list'),
    path('digests/fresh/', FreshDigestView.as_view(), name='digest-fresh'),
    path('articles/', NewsArticleListView.as_view(), name='article-list'),
    path('digests/sections/', FreshDigestSectionsView.as_view(), name='digest-sections'),
] 