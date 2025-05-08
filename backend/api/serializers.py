from rest_framework import serializers
from core.models import Story, KeywordMention, DomainStats

class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = [
            'id', 'title', 'url', 'domain', 'score', 
            'comments_count', 'author', 'timestamp', 
            'is_ai_related'
        ]

class KeywordMentionSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeywordMention
        fields = ['keyword', 'story']

class DomainStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DomainStats
        fields = ['domain', 'count', 'last_updated']

class KeywordFrequencySerializer(serializers.Serializer):
    keyword = serializers.CharField()
    count = serializers.IntegerField()
