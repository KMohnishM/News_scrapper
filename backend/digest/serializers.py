from rest_framework import serializers
from .models import NewsArticle, Digest, UserPreferences

class NewsArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsArticle
        fields = '__all__'

class DigestSerializer(serializers.ModelSerializer):
    articles = NewsArticleSerializer(many=True, read_only=True)
    class Meta:
        model = Digest
        fields = '__all__'

class UserPreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreferences
        fields = '__all__' 