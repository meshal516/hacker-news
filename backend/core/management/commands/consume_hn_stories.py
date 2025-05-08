import json
import logging
import time
from django.core.management.base import BaseCommand
from django.conf import settings
from confluent_kafka import Consumer, KafkaError, KafkaException

from tasks import FETCH_STORIES_TOPIC, fetch_top_stories_logic, producer_config as base_producer_config

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Runs the Kafka consumer for fetching Hacker News stories triggered by messages.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting Kafka consumer for Hacker News stories fetch...'))

        if not settings.KAFKA_BOOTSTRAP_SERVERS or settings.KAFKA_BOOTSTRAP_SERVERS == 'your_kafka_bootstrap_servers':
            self.stderr.write(self.style.ERROR(
                'Kafka bootstrap servers are not configured or are using placeholders. Exiting consumer.'
            ))
            return

        # Consumer config uses the same base settings as producer for bootstrap, security, etc.
        consumer_conf = {
            **base_producer_config, # Re-use producer config for server details & auth
            'group.id': f'{settings.KAFKA_TOPIC_PREFIX}fetch_stories_consumer_group', # Unique consumer group ID
            'auto.offset.reset': 'earliest', # Start reading at the earliest offset if no offset is stored
        }

        consumer = None
        try:
            consumer = Consumer(consumer_conf)
            consumer.subscribe([FETCH_STORIES_TOPIC])
            self.stdout.write(f'Subscribed to Kafka topic: {FETCH_STORIES_TOPIC}')

            while True:
                msg = consumer.poll(timeout=1.0)  # Poll for new messages with a 1-second timeout

                if msg is None:
                    continue # No message_received, keep polling
                
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        # End of partition event
                        logger.info(f'%% {msg.topic()} [{msg.partition()}] reached end at offset {msg.offset()}')
                    elif msg.error():
                        # Actual error
                        logger.error(f'Kafka error: {msg.error()}')
                        time.sleep(5) # Wait before retrying to connect or poll
                    continue

                # Message successfully consumed
                try:
                    payload = json.loads(msg.value().decode('utf-8'))
                    self.stdout.write(f'Received message from {msg.topic()}: {payload}')
                    logger.info(f"Processing message from {msg.topic()} with key {msg.key()}: {payload}")

                    # Call the actual logic function from tasks.py
                    result = fetch_top_stories_logic(message_payload=payload)

                    if result.get("status") == "success":
                        self.stdout.write(self.style.SUCCESS(
                            f"Successfully processed HN story fetch from Kafka message: "
                            f"{result.get('processed_stories', 0)} processed, "
                            f"{result.get('new', 0)} new, "
                            f"{result.get('updated', 0)} updated."
                        ))
                    else:
                        self.stderr.write(self.style.ERROR(
                            f"Failed to process HN story fetch from Kafka message: {result.get('reason', 'Unknown error')}"
                        ))
                    

                except json.JSONDecodeError as e:
                    logger.error(f"Error decoding JSON payload: {msg.value().decode('utf-8')} - {e}")
                    self.stderr.write(self.style.ERROR(f"Could not decode message payload: {e}"))
                except Exception as e:
                    logger.error(f"Error processing message payload {msg.value().decode('utf-8')}: {e}", exc_info=True)
                    self.stderr.write(self.style.ERROR(f"Error processing message: {e}"))

        except KafkaException as ke:
            logger.error(f"KafkaException encountered: {ke}", exc_info=True)
            self.stderr.write(self.style.ERROR(f"Critical Kafka error: {ke}. Consumer will exit."))
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING(' Kafka consumer interrupted by user.'))
        except Exception as e:
            logger.error(f"Unexpected error in Kafka consumer: {e}", exc_info=True)
            self.stderr.write(self.style.ERROR(f"An unexpected critical error occurred: {e}. Consumer will exit."))
        finally:
            if consumer:
                consumer.close()
                self.stdout.write(self.style.SUCCESS('Kafka consumer closed.')) 