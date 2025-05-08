from django.apps import AppConfig
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        # This method is called once Django is ready.
        logger.info("CoreConfig.ready(): Application ready. Performing startup tasks...")

        # --- 1. Clear Cache ---
        if hasattr(cache, 'delete_pattern'):
            patterns_to_clear = [
                "stories_list_*",       # Covers all filtered and unfiltered story lists
                "story_*",              # Covers individual cached stories
                "ai_keywords",          # Fixed key for AI keyword frequencies
                "top_domains_limit_*",  # Covers all top domain lists with different limits
            ]
            for pattern in patterns_to_clear:
                try:
                    cache.delete_pattern(pattern)
                    logger.info(f"CoreConfig.ready(): Cleared cache pattern: {pattern}")
                except Exception as e:
                    logger.error(f"CoreConfig.ready(): Error clearing cache pattern {pattern}: {e}")
            
        else:
            logger.warning("CoreConfig.ready(): Cache backend does not support delete_pattern. Clearing specific keys only.")
            # Fallback for cache backends that don't support delete_pattern
            keys_to_clear = ['stories_list', 'ai_keywords', 'top_domains'] # Add more specific keys if needed
            for key in keys_to_clear:
                cache.delete(key)
                logger.info(f"CoreConfig.ready(): Cleared specific cache key: {key}")

        # --- 2. Schedule Initial Data Fetch ---
        # Import dynamically to avoid circular imports if tasks.py imports models from core
        try:
            from tasks import schedule_fetch_top_stories_task # Ensure tasks.py is in PYTHONPATH
            
            # Check if Kafka producer is available before scheduling
            # This check can be made more robust based on how kafka_producer is initialized in tasks.py
            from tasks import kafka_producer 
            if kafka_producer:
                if schedule_fetch_top_stories_task():
                    logger.info("CoreConfig.ready(): Successfully scheduled initial fetch of top stories.")
                else:
                    logger.warning("CoreConfig.ready(): Failed to schedule initial fetch of top stories (Kafka producer might be unavailable or issue with send).")
            else:
                logger.warning("CoreConfig.ready(): Kafka producer not available in tasks.py. Initial story fetch not scheduled.")
        except ImportError:
            logger.error("CoreConfig.ready(): Could not import 'schedule_fetch_top_stories_task' from tasks.py. Check PYTHONPATH and circular dependencies.")
        except Exception as e:
            logger.error(f"CoreConfig.ready(): Error during initial task scheduling: {e}")

        logger.info("CoreConfig.ready(): Startup tasks complete.") 