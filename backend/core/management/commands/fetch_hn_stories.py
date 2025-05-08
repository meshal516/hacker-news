import logging
from django.core.management.base import BaseCommand

from tasks import fetch_top_stories_logic

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Fetches top stories from Hacker News and populates the database.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to fetch Hacker News stories...'))
        
        try:
            # The `fetch_top_stories_logic` function in tasks.py expects an optional
            # message_payload argument if triggered by Kafka. For a direct call,
            # we can pass None or a dummy dict.
            result = fetch_top_stories_logic(message_payload={'source': 'management_command'})
            
            if result.get("status") == "success":
                self.stdout.write(self.style.SUCCESS(
                    f"Successfully processed stories: "
                    f"{result.get('processed_stories', 0)} processed, "
                    f"{result.get('new', 0)} new, "
                    f"{result.get('updated', 0)} updated."
                ))
            else:
                self.stderr.write(self.style.ERROR(
                    f"Failed to process stories: {result.get('reason', 'Unknown error')}"
                ))
        except Exception as e:
            logger.error(f"Error during fetch_hn_stories command: {e}", exc_info=True)
            self.stderr.write(self.style.ERROR(f"An unexpected error occurred: {e}"))

        self.stdout.write(self.style.SUCCESS('Finished fetching Hacker News stories.')) 