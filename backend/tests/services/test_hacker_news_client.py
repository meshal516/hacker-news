import pytest
import requests
import time
from datetime import datetime
from services.hacker_news import HackerNewsClient


def test_get_top_stories_success(requests_mock):
    """Test fetching top stories successfully."""
    mock_ids = list(range(1, 60))
    requests_mock.get(f"{HackerNewsClient.BASE_URL}/topstories.json", json=mock_ids)
    
    story_ids = HackerNewsClient.get_top_stories(limit=50)
    assert story_ids == list(range(1, 51))
    assert len(story_ids) == 50

def test_get_top_stories_failure(requests_mock):
    """Test failure when fetching top stories."""
    requests_mock.get(f"{HackerNewsClient.BASE_URL}/topstories.json", status_code=500)
    
    story_ids = HackerNewsClient.get_top_stories(limit=50)
    assert story_ids == []

def test_get_story_details_success(requests_mock):
    """Test fetching story details successfully."""
    story_id = 12345
    mock_time = int(time.time())
    mock_response = {
        'id': story_id,
        'title': 'Test Story Title',
        'url': 'http://example.com/story',
        'score': 100,
        'descendants': 50,
        'by': 'testuser',
        'time': mock_time,
    }
    requests_mock.get(f"{HackerNewsClient.BASE_URL}/item/{story_id}.json", json=mock_response)
    
    details = HackerNewsClient.get_story_details(story_id)
    assert details is not None
    assert details['id'] == story_id
    assert details['title'] == 'Test Story Title'
    assert details['url'] == 'http://example.com/story'
    assert details['domain'] == 'example.com' # Check domain extraction
    assert details['score'] == 100
    assert details['comments_count'] == 50
    assert details['author'] == 'testuser'
    assert isinstance(details['timestamp'], datetime)
    assert details['timestamp'] == datetime.fromtimestamp(mock_time)

def test_get_story_details_missing_fields(requests_mock):
    """Test fetching story details with missing crucial fields (like title)."""
    story_id = 54321
    mock_response = {'id': story_id, 'by': 'user'} # Missing title
    requests_mock.get(f"{HackerNewsClient.BASE_URL}/item/{story_id}.json", json=mock_response)
    
    details = HackerNewsClient.get_story_details(story_id)
    assert details is None

def test_get_story_details_no_url(requests_mock):
    """Test fetching story details when URL is missing."""
    story_id = 67890
    mock_time = int(time.time())
    mock_response = {
        'id': story_id,
        'title': 'Ask HN: Test',
        'score': 10,
        'descendants': 5,
        'by': 'asker',
        'time': mock_time,
    }
    requests_mock.get(f"{HackerNewsClient.BASE_URL}/item/{story_id}.json", json=mock_response)
    
    details = HackerNewsClient.get_story_details(story_id)
    assert details is not None
    assert details['id'] == story_id
    assert details['title'] == 'Ask HN: Test'
    assert details['url'] == '' # URL should default to empty string
    assert details['domain'] is None # Domain should be None if no URL

def test_get_story_details_failure(requests_mock):
    """Test failure when fetching story details."""
    story_id = 99999
    requests_mock.get(f"{HackerNewsClient.BASE_URL}/item/{story_id}.json", exc=requests.exceptions.RequestException)
    
    details = HackerNewsClient.get_story_details(story_id)
    assert details is None 