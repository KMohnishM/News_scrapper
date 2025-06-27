from django.shortcuts import render
from rest_framework import generics
from .models import Digest, NewsArticle
from .serializers import DigestSerializer, NewsArticleSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .tasks import create_news_and_summaries, build_digest
import logging

# Create your views here.

class DigestListView(generics.ListAPIView):
    queryset = Digest.objects.order_by('-date')
    serializer_class = DigestSerializer

class NewsArticleListView(generics.ListAPIView):
    queryset = NewsArticle.objects.order_by('-published_at')
    serializer_class = NewsArticleSerializer

class FreshDigestView(APIView):
    def get(self, request, *args, **kwargs):
        digest = create_news_and_summaries()
        serializer = DigestSerializer(digest)
        logger = logging.getLogger(__name__)
        logger.info(f"FreshDigestView response: {serializer.data}")
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class FreshDigestSectionsView(APIView):
    def get(self, request, *args, **kwargs):
        digest_sections = build_digest()
        return Response(digest_sections, status=status.HTTP_200_OK)
