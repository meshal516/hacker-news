import logging
from django.core.management.base import BaseCommand
from django.conf import settings


from tasks import schedule_fetch_top_stories_task

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Sends a message to Kafka to trigger fetching of Hacker News stories.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Attempting to schedule Hacker News stories fetch via Kafka...'))

        if not settings.KAFKA_BOOTSTRAP_SERVERS or settings.KAFKA_BOOTSTRAP_SERVERS == 'your_kafka_bootstrap_servers':
            self.stderr.write(self.style.ERROR(
                'Kafka bootstrap servers are not configured or are using placeholders. Cannot schedule task.'
            ))
            return

        try:
            success = schedule_fetch_top_stories_task()
            if success:
                self.stdout.write(self.style.SUCCESS(
                    'Successfully sent message to Kafka to trigger Hacker News stories fetch.'
                ))
            else:
                self.stderr.write(self.style.ERROR(
                    'Failed to send message to Kafka to trigger Hacker News stories fetch. Check logs in tasks.py.'
                ))
        except Exception as e:
            logger.error(f"Error during schedule_hn_fetch command: {e}", exc_info=True)
            self.stderr.write(self.style.ERROR(f"An unexpected error occurred while trying to schedule task: {e}")) 