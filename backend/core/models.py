from django.db import models
from django.utils import timezone

class Story(models.Model):
    """Model for storing HackerNews stories"""
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=500)
    url = models.URLField(max_length=2000, null=True, blank=True)
    domain = models.CharField(max_length=255, null=True, blank=True)
    score = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)
    author = models.CharField(max_length=255)
    timestamp = models.DateTimeField()
    fetched_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_ai_related = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title

class KeywordMention(models.Model):
    """Model for tracking AI-related keyword mentions"""
    keyword = models.CharField(max_length=100)
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='keywords')
    
    class Meta:
        unique_together = ('keyword', 'story')
    
    def __str__(self):
        return f"{self.keyword} in {self.story.id}"

class DomainStats(models.Model):
    """Model for tracking domain statistics"""
    domain = models.CharField(max_length=255, unique=True)
    count = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.domain} ({self.count})"
