import requests
import logging
from datetime import datetime
from django.conf import settings
from urllib.parse import urlparse
import time

logger = logging.getLogger(__name__)

class HackerNewsClient:
    """Client for interacting with the HackerNews API"""
    BASE_URL = "https://hacker-news.firebaseio.com/v0"
    DEFAULT_TIMEOUT = 15 # seconds
    
    @classmethod
    def get_top_stories(cls, limit=50):
        """Fetch IDs of top stories"""
        try:
            response = requests.get(f"{cls.BASE_URL}/topstories.json", timeout=cls.DEFAULT_TIMEOUT)
            response.raise_for_status()
            story_ids = response.json()
            logger.info(f"Fetched {len(story_ids)} top story IDs from API.")
            return story_ids[:limit]
        except requests.RequestException as e:
            logger.error(f"Error fetching top stories: {e}")
            return []
    
    @classmethod
    def get_story_details(cls, story_id):
        """Fetch details for a specific story"""
        try:
            response = requests.get(f"{cls.BASE_URL}/item/{story_id}.json", timeout=cls.DEFAULT_TIMEOUT)
            response.raise_for_status()
            data = response.json()
            
            # Transform and validate the data
            if not data or 'title' not in data:
                return None
                
            # Extract domain from URL if present
            domain = None
            if 'url' in data and data['url']:
                parsed_url = urlparse(data['url'])
                domain = parsed_url.netloc
            
            return {
                'id': data.get('id'),
                'title': data.get('title', ''),
                'url': data.get('url', ''),
                'domain': domain,
                'score': data.get('score', 0),
                'comments_count': data.get('descendants', 0),
                'author': data.get('by', ''),
                'timestamp': datetime.fromtimestamp(data.get('time', 0)),
            }
        except requests.RequestException as e:
            logger.error(f"Error fetching story {story_id}: {e}")
            return None
