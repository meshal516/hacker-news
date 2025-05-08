import json
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from confluent_kafka import Producer, KafkaError
from django.utils import timezone
from django.db import transaction # Import transaction for atomicity
from django.db.models import F
from django.core.cache import cache
from django.conf import settings

from core.models import Story, KeywordMention, DomainStats
from services.hacker_news import HackerNewsClient
from services.keyword_detector import KeywordDetector

logger = logging.getLogger(__name__)

# Kafka Topics
FETCH_STORIES_TOPIC = f"{settings.KAFKA_TOPIC_PREFIX}fetch_stories"

# Kafka Producer Configuration
producer_config = {
    'bootstrap.servers': settings.KAFKA_BOOTSTRAP_SERVERS,
    'security.protocol': settings.KAFKA_SECURITY_PROTOCOL,
    'sasl.mechanisms': settings.KAFKA_SASL_MECHANISM,
    'sasl.username': settings.KAFKA_SASL_USERNAME,
    'sasl.password': settings.KAFKA_SASL_PASSWORD,
}

kafka_producer = None
try:
    if settings.KAFKA_BOOTSTRAP_SERVERS and settings.KAFKA_BOOTSTRAP_SERVERS != 'your_kafka_bootstrap_servers': # Avoid creating producer with placeholder
        kafka_producer = Producer(producer_config)
        logger.info("Kafka producer initialized successfully.")
    else:
        logger.warning("Kafka producer not initialized due to missing or placeholder configuration.")
except KafkaError as e:
    logger.error(f"Failed to initialize Kafka producer: {e}")
    kafka_producer = None


def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result. """
    if err is not None:
        logger.error(f'Message delivery failed: {err}')
    else:
        logger.info(f'Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}')

def send_kafka_message(topic, message_key, message_payload):
    if not kafka_producer:
        logger.error(f"Kafka producer not available. Cannot send message to topic {topic}")
        return False
    try:
        kafka_producer.produce(
            topic,
            key=str(message_key).encode('utf-8'),
            value=json.dumps(message_payload).encode('utf-8'),
            callback=delivery_report
        )
        kafka_producer.poll(0) # Trigger delivery report callbacks
        return True
    except BufferError:
        logger.error(f"Kafka local producer queue is full ({len(kafka_producer)} messages awaiting delivery): try again")
        return False
    except Exception as e:
        logger.error(f"Error sending message to Kafka topic {topic}: {e}")
        return False

# --- Task Scheduling Functions (to be called by a scheduler) ---

def schedule_fetch_top_stories_task():
    """Sends a message to Kafka to trigger fetching top stories."""
    payload = {'task_type': 'fetch_top_stories', 'timestamp': timezone.now().isoformat()}
    if send_kafka_message(FETCH_STORIES_TOPIC, 'fetch_trigger', payload):
        logger.info(f"Successfully scheduled 'fetch_top_stories' task via Kafka.")
        return True
    logger.error(f"Failed to schedule 'fetch_top_stories' task via Kafka.")
    return False


# --- Core Task Logic (to be called by Kafka Consumers) ---

MAX_WORKERS = 10 # Number of concurrent workers for fetching story details

def _fetch_and_process_story_details(story_id):
    """Helper function to fetch details and prepare data for a single story."""
    story_data = HackerNewsClient.get_story_details(story_id)
    if not story_data:
        logger.warning(f"No data retrieved for story ID {story_id}")
        return None # Indicate failure for this ID
    
    # Calculate AI related status
    story_is_ai_related = False
    ai_keywords_found = []
    title = story_data.get('title')
    if title:
        ai_keywords_found = KeywordDetector.find_ai_keywords(title)
        story_is_ai_related = len(ai_keywords_found) > 0
        
    # Return processed data including the AI flag and keywords
    processed_data = {
        'db_data': { # Data intended for DB update_or_create
            'id': story_data['id'],
            'title': story_data.get('title', ''), 
            'url': story_data.get('url', ''),
            'domain': story_data.get('domain'), 
            'score': story_data.get('score', 0),
            'comments_count': story_data.get('comments_count', 0),
            'author': story_data.get('author', ''),
            'timestamp': story_data.get('timestamp'), 
            'is_ai_related': story_is_ai_related,
        },
        'cache_data': story_data, # Original data for cache
        'ai_keywords_found': ai_keywords_found,
    }
    return processed_data

def fetch_top_stories_logic(message_payload=None):
    """Fetch top stories concurrently and save to database."""
    logger.info(f"Executing fetch_top_stories_logic. Triggered by: {message_payload}")
    
    # Get top story IDs (using limit from spec, default in HackerNewsClient is 50)
    story_ids = HackerNewsClient.get_top_stories()
    if not story_ids:
        logger.warning("No story IDs retrieved from HackerNews API")
        return {"status": "failure", "reason": "No story IDs retrieved"}

    logger.info(f"Fetched {len(story_ids)} top story IDs. Fetching details concurrently...")

    new_count = 0
    updated_count = 0
    processed_story_count = 0
    failed_fetches = 0
    
    # Use ThreadPoolExecutor for concurrent fetching
    processed_results = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # Submit all fetch tasks
        future_to_id = {executor.submit(_fetch_and_process_story_details, story_id): story_id for story_id in story_ids}
        
        # Process results as they complete
        processed_count_fetch = 0 # Counter for logging fetch progress
        for future in as_completed(future_to_id):
            story_id = future_to_id[future]
            processed_count_fetch += 1
            try:
                result_data = future.result()
                if result_data: # Check if fetching and processing succeeded
                    processed_results.append(result_data)
                    if processed_count_fetch % 10 == 0: # Log every 10 fetches
                        logger.info(f"Fetched details for {processed_count_fetch}/{len(story_ids)} stories...")
                else:
                    failed_fetches += 1
                    logger.warning(f"Failed to fetch/process details for story {story_id} (attempt {processed_count_fetch}/{len(story_ids)}).")
            except Exception as exc:
                logger.error(f'Story ID {story_id} generated an exception during fetch/process (attempt {processed_count_fetch}/{len(story_ids)}): {exc}', exc_info=False) # Keep log less verbose
                failed_fetches += 1

    logger.info(f"Finished fetching details. Processing {len(processed_results)} successful results in database.")

    stories_to_update_or_create = []
    keyword_mentions_to_create = []
    story_ids_processed_db = set()

    for result in processed_results:
        db_data = result['db_data']
        cache_data = result['cache_data']
        ai_keywords = result['ai_keywords_found']
        story_id = db_data['id']

        stories_to_update_or_create.append(db_data)
        story_ids_processed_db.add(story_id)

        # Add keywords for bulk creation later
        for keyword in ai_keywords:
            keyword_mentions_to_create.append({'keyword': keyword, 'story_id': story_id})
            
        # Cache the data
        cache.set(f"story_{story_id}", cache_data, timeout=60 * 60 * 24)
        

  

    # --- Perform Database Operations --- 
    try:
        # Use a transaction for atomicity
        with transaction.atomic():
            # Loop through successfully fetched stories for DB update/create
            processed_db_count_log = 0 # Counter for logging DB progress
            for story_data in stories_to_update_or_create:
                story_id = story_data['id']
                defaults = story_data # The whole dict contains the defaults
                created = Story.objects.update_or_create(id=story_id, defaults=defaults)
                processed_db_count_log += 1 # Increment after processing
                if created:
                    new_count += 1
                    # Handle domain count for newly created stories
                    domain = story_data.get('domain')
                    if domain:
                         DomainStats.objects.get_or_create(
                            domain=domain,
                            defaults={'count': 0} 
                         )
                         # Use F expression for atomic increment
                         DomainStats.objects.filter(domain=domain).update(count=F('count') + 1)
                else:
                    updated_count += 1
                processed_story_count += 1 # This counts stories successfully processed in DB
                
                # Log progress every 10 DB operations
                if processed_db_count_log % 10 == 0:
                    logger.info(f"Database update progress: {processed_db_count_log}/{len(stories_to_update_or_create)} stories processed...")
            
            logger.info(f"Finished story DB updates/creates.")
            

            keyword_mentions_created_count = 0
            for mention in keyword_mentions_to_create:
                 _, created_kw = KeywordMention.objects.get_or_create(
                     keyword=mention['keyword'],
                     story_id=mention['story_id'] # Use story_id directly
                 )
                 if created_kw:
                     keyword_mentions_created_count += 1
            logger.info(f"Created {keyword_mentions_created_count} new KeywordMention records.")

    except Exception as e:
        logger.error(f"Database transaction failed during story update/create: {e}", exc_info=True)
        # Depending on the error, we might have partial updates.
        return {"status": "failure", "reason": f"Database transaction failed: {e}"}

    logger.info(f"Processed {processed_story_count} stories in DB: {new_count} new, {updated_count} updated. {failed_fetches} failed fetches.")

    # Clear relevant cache keys using patterns since django-redis is used
    if hasattr(cache, 'delete_pattern'):
        logger.info("tasks.py: Clearing cache patterns after story fetch.")
        cache.delete_pattern("stories_list_*")
        cache.delete_pattern("story_*")
        cache.delete("ai_keywords") # This is a fixed key
        cache.delete_pattern("top_domains_limit_*")
    else:
        logger.warning("tasks.py: Cache backend does not support delete_pattern. Clearing specific keys only.")
        cache.delete('stories_list') 
        cache.delete('ai_keywords')
        cache.delete('top_domains')

    return {
        "status": "success", 
        "processed_stories": processed_story_count, 
        "new": new_count, 
        "updated": updated_count,
        "failed_fetches": failed_fetches
    }
