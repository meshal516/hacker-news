from django.utils import timezone
from django.db.models import Count
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.cache import cache

from core.models import Story, KeywordMention, DomainStats
from .serializers import (
    StorySerializer, KeywordMentionSerializer, 
    DomainStatsSerializer, KeywordFrequencySerializer
)

class StoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for stories
    """
    queryset = Story.objects.all().order_by('-timestamp')
    serializer_class = StorySerializer
    
    def get_queryset(self):
        queryset = Story.objects.all().order_by('-timestamp')
        
        # Apply filters if provided
        keyword = self.request.query_params.get('keyword')
        if keyword:
            queryset = queryset.filter(title__icontains=keyword)
        
        is_ai_related = self.request.query_params.get('is_ai_related')
        if is_ai_related:
            is_ai = is_ai_related.lower() == 'true'
            queryset = queryset.filter(is_ai_related=is_ai)
            
        domain = self.request.query_params.get('domain')
        if domain:
            queryset = queryset.filter(domain__icontains=domain)
            
        start_date = self.request.query_params.get('start_date')
        if start_date:
            queryset = queryset.filter(timestamp__gte=start_date)
            
        end_date = self.request.query_params.get('end_date')
        if end_date:
            queryset = queryset.filter(timestamp__lte=end_date)
            
        return queryset
    
    def list(self, request, *args, **kwargs):
        """Cache the stories list to improve performance"""
        cache_key = 'stories_list'
        # Generate a unique cache key based on query parameters
        if request.query_params:
            param_str = "&".join([f"{k}={v}" for k, v in request.query_params.items()])
            cache_key = f"{cache_key}_{param_str}"
        
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)
        
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        cache.set(cache_key, serializer.data, timeout=60*5)  # Cache for 5 minutes
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        """Cache individual story retrieval"""
        pk = kwargs.get('pk')
        cache_key = f"story_{pk}"
        cached_story = cache.get(cache_key)

        if cached_story:
            return Response(cached_story)

        instance = self.get_object()
        serializer = self.get_serializer(instance)
        # Cache the serialized data for consistency with list view if that's preferred
        cache.set(cache_key, serializer.data, timeout=60 * 60 * 24) # Cache for 24 hours
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def ai_related(self, request):
        """Get only AI-related stories"""
        queryset = Story.objects.filter(is_ai_related=True).order_by('-timestamp')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class InsightsViewSet(viewsets.ViewSet):
    """
    API endpoint for insights and aggregated data
    """
    
    @action(detail=False, methods=['get'])
    def keyword_frequency(self, request):
        """Get frequency of AI-related keywords"""
        cache_key = 'ai_keywords'
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return Response(cached_data)
        
        # Count keyword occurrences
        keyword_counts = KeywordMention.objects.values('keyword').annotate(
            count=Count('keyword')
        ).order_by('-count')
        
        serializer = KeywordFrequencySerializer(keyword_counts, many=True)
        cache.set(cache_key, serializer.data, timeout=60*10)  # Cache for 10 minutes
        
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def top_domains(self, request):
        """Get top domains by frequency"""
        cache_key = 'top_domains'
        limit = int(request.query_params.get('limit', 10))
        
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data[:limit])
        
        domains = DomainStats.objects.all().order_by('-count')[:limit]
        serializer = DomainStatsSerializer(domains, many=True)
        
        cache.set(cache_key, serializer.data, timeout=60*10)  # Cache for 10 minutes
        
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def stats_summary(self, request):
        """Get overall statistics summary"""
        total_stories = Story.objects.count()
        ai_related_count = Story.objects.filter(is_ai_related=True).count()
        domains_count = DomainStats.objects.count()
        avg_score = Story.objects.all().aggregate(Avg('score'))['score__avg'] or 0
        avg_comments = Story.objects.all().aggregate(Avg('comments_count'))['comments_count__avg'] or 0
        
        data = {
            'total_stories': total_stories,
            'ai_related_count': ai_related_count,
            'ai_percentage': (ai_related_count / total_stories * 100) if total_stories > 0 else 0,
            'unique_domains': domains_count,
            'avg_score': round(avg_score, 2),
            'avg_comments': round(avg_comments, 2),
        }
        
        return Response(data)
