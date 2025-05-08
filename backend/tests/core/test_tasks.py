import pytest
from unittest.mock import patch, MagicMock, call
from datetime import datetime

from django.utils import timezone
from django.core.cache import cache
from django.db.models import F

from core.models import Story, KeywordMention, DomainStats
from tasks import fetch_top_stories_logic
from services.keyword_detector import KeywordDetector # Import for potential direct mocking if needed

@pytest.fixture
def mock_hn_client(mocker): # Use pytest-mock fixture
    # Mock the class methods directly on the HackerNewsClient class imported into tasks module
    # The HackerNewsClient class itself is located in services.hacker_news
    # tasks.py imports it as: from services.hacker_news import HackerNewsClient
    
    # Default behavior for get_top_stories
    mock_get_top = mocker.patch('tasks.HackerNewsClient.get_top_stories', return_value=[1, 2, 3])
    
    # Default behavior for get_story_details
    def side_effect_get_details(story_id):
        mock_time = timezone.now()
        if story_id == 1:
            return {
                'id': 1, 'title': 'Story about OpenAI', 'url': 'http://openai.com', 
                'domain': 'openai.com', 'score': 10, 'comments_count': 5, 
                'author': 'user1', 'timestamp': mock_time
            }
        elif story_id == 2:
            return {
                'id': 2, 'title': 'New LLM Framework Released', 'url': 'http://llm-framework.com',
                'domain': 'llm-framework.com', 'score': 5, 'comments_count': 2, 
                'author': 'user2', 'timestamp': mock_time
            }
        elif story_id == 3:
            return None # Simulate failure for one ID
        return None
    mock_get_details = mocker.patch('tasks.HackerNewsClient.get_story_details', side_effect=side_effect_get_details)
    
    # Return the mocked methods themselves, or a simple object that can be used 
    # by tests to change return_values if needed (though it's often cleaner to re-patch in the test).
    # For tests that just rely on default behavior, this fixture sets it up.
    # For tests that need to change behavior (like test_fetch_top_stories_no_ids),
    # they will re-patch tasks.HackerNewsClient.get_top_stories directly.
    class MockHNMocks:
        def __init__(self):
            self.get_top_stories = mock_get_top
            self.get_story_details = mock_get_details
            
    return MockHNMocks()

@pytest.fixture
def mock_keyword_detector(mocker):
    # Define the side effect function for find_ai_keywords
    def side_effect_find_keywords(title_text):
        found_keywords = []
        if isinstance(title_text, str): # Ensure title_text is a string
            if 'OpenAI' in title_text or 'openai' in title_text.lower():
                found_keywords.append('openai')
            if 'LLM' in title_text or 'llm' in title_text.lower():
                found_keywords.extend(['llm', 'large language model']) # As per KeywordDetector logic
        return list(set(found_keywords)) # Return unique keywords

    # Patch the find_ai_keywords method directly on the KeywordDetector class
    # as it's imported and used in the 'tasks' module.
    # tasks.py calls: KeywordDetector.find_ai_keywords(title)
    mocker.patch('tasks.KeywordDetector.find_ai_keywords', side_effect=side_effect_find_keywords)
    
    # The fixture can just return the mocker object or None, as the patch is the main thing.
    # For consistency, if other tests might want to inspect the mock itself (though less common for static/class method patches):
    return mocker.patch # Or return the specific mock object if needed later, e.g. tasks.KeywordDetector.find_ai_keywords

@pytest.fixture
def mock_cache(mocker):
    # Simple mock, doesn't fully replicate cache behavior but allows checking calls
    mocker.patch.object(cache, 'set')
    mocker.patch.object(cache, 'delete')
    mocker.patch.object(cache, 'get', return_value=None) # Assume cache miss
    return cache



@pytest.mark.django_db(transaction=True)
def test_fetch_top_stories_logic_update(
    mock_hn_client, mock_keyword_detector, mock_cache
):
    """Test updating an existing story."""
    # Pre-populate story 1
    Story.objects.create(
        id=1, title='Old Title', url='http://old.com', 
        domain='old.com', score=5, comments_count=1, 
        author='olduser', timestamp=timezone.now(), is_ai_related=False
    )
    assert Story.objects.count() == 1
    
    result = fetch_top_stories_logic()
    
    assert result['status'] == 'success'
    assert result['processed_stories'] == 2
    assert result['new'] == 2
    assert result['updated'] == 0
    assert result['failed_fetches'] == 1
    
    # Check updated story 1
    story1 = Story.objects.get(id=1)
    assert story1.title == 'Story about OpenAI'
    assert story1.is_ai_related is True
    assert KeywordMention.objects.filter(story_id=1).count() == 1
    assert KeywordMention.objects.get(story_id=1, keyword='openai')

@pytest.mark.django_db # Added django_db marker
def test_fetch_top_stories_no_ids(mock_hn_client, mocker): # Add mocker to re-patch
    """Test when HackerNewsClient returns no story IDs."""
    # Override the get_top_stories mock for this specific test
    mocker.patch('tasks.HackerNewsClient.get_top_stories', return_value=[])
    result = fetch_top_stories_logic()
    assert result['status'] == 'failure'
    assert result['reason'] == 'No story IDs retrieved' 