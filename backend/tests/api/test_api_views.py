import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient
from core.models import Story, KeywordMention, DomainStats
from django.core.cache import cache

@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_list_stories_with_data(api_client):
    cache.delete('stories_list') # Base cache key used in StoryViewSet

    story1 = Story.objects.create(
        id=101, title='AI Story', url='', score=10, author='u1', 
        timestamp=timezone.now(), is_ai_related=True
    )
    story2 = Story.objects.create(
        id=102, title='Non AI Story', url='', score=5, author='u2',
        timestamp=timezone.now(), is_ai_related=False
    )
    
    url = reverse('story-list')
    response = api_client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]['id'] == story2.id # Default ordering is -timestamp, assuming story2 is newer
    assert data[1]['id'] == story1.id

@pytest.mark.django_db
def test_retrieve_story(api_client):
    story = Story.objects.create(
        id=103, title='Specific Story', url='', score=20, author='u3',
        timestamp=timezone.now(), is_ai_related=False
    )
    url = reverse('story-detail', kwargs={'pk': story.id})
    response = api_client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == story.id
    assert data['title'] == 'Specific Story'

@pytest.mark.django_db
def test_retrieve_story_not_found(api_client):
    url = reverse('story-detail', kwargs={'pk': 999})
    response = api_client.get(url)
    assert response.status_code == 404

@pytest.mark.django_db
def test_list_stories_filter_ai_related(api_client):
    Story.objects.create(id=201, title='AI Story 1', is_ai_related=True, author='a', timestamp=timezone.now())
    Story.objects.create(id=202, title='Non AI Story', is_ai_related=False, author='b', timestamp=timezone.now())
    Story.objects.create(id=203, title='AI Story 2', is_ai_related=True, author='c', timestamp=timezone.now())
    
    url = reverse('story-list') + '?is_ai_related=true'
    response = api_client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]['id'] == 203 # Assuming newer
    assert data[1]['id'] == 201

    url_false = reverse('story-list') + '?is_ai_related=false'
    response_false = api_client.get(url_false)
    assert response_false.status_code == 200
    data_false = response_false.json()
    assert len(data_false) == 1
    assert data_false[0]['id'] == 202

@pytest.mark.django_db
def test_keyword_frequency_endpoint(api_client):
    story1 = Story.objects.create(id=301, title='Test OpenAI', author='a', timestamp=timezone.now())
    story2 = Story.objects.create(id=302, title='Test LLM', author='b', timestamp=timezone.now())
    story3 = Story.objects.create(id=303, title='Another OpenAI test', author='c', timestamp=timezone.now())
    KeywordMention.objects.create(keyword='openai', story=story1)
    KeywordMention.objects.create(keyword='llm', story=story2)
    KeywordMention.objects.create(keyword='openai', story=story3)
    
    url = reverse('insights-keyword-frequency') # Action names use hyphens
    response = api_client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    # Default ordering is by count desc
    assert data[0] == {'keyword': 'openai', 'count': 2}
    assert data[1] == {'keyword': 'llm', 'count': 1}

@pytest.mark.django_db
def test_top_domains_endpoint(api_client):
    DomainStats.objects.create(domain='example.com', count=10)
    DomainStats.objects.create(domain='test.org', count=5)
    DomainStats.objects.create(domain='another.net', count=15)
    
    url = reverse('insights-top-domains')
    response = api_client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3 # Default limit is 10, we have 3
    assert data[0]['domain'] == 'another.net' # Ordered by count desc
    assert data[0]['count'] == 15
    assert data[1]['domain'] == 'example.com'
    assert data[2]['domain'] == 'test.org'

    url_limit = reverse('insights-top-domains') + '?limit=1'
    response_limit = api_client.get(url_limit)
    assert response_limit.status_code == 200
    data_limit = response_limit.json()
    assert len(data_limit) == 1
    assert data_limit[0]['domain'] == 'another.net' 