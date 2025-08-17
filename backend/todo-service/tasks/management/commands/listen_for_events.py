import json
import time
from django.core.management.base import BaseCommand
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable
from tasks.models import Todo


class Command(BaseCommand):
    help = "Listen for Kafka events"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("--> Starting Kafka Consumer..."))

        consumer = None
        # Retry connecting to Kafka in case it's not ready yet
        for _ in range(5):  # Retry 5 times
            try:
                consumer = KafkaConsumer(
                    "user_deleted_topic",
                    bootstrap_servers="kafka:9092",
                    auto_offset_reset="earliest",
                    group_id="todo-service-group",
                    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
                )
                self.stdout.write(
                    self.style.SUCCESS("--> Kafka Consumer connected successfully!")
                )
                break  # Exit loop if connection is successful
            except NoBrokersAvailable:
                self.stdout.write(
                    self.style.WARNING(
                        "--> Kafka not available, retrying in 5 seconds..."
                    )
                )
                time.sleep(5)

        if not consumer:
            self.stdout.write(
                self.style.ERROR(
                    "--> Could not connect to Kafka after multiple retries. Exiting."
                )
            )
            return

        self.stdout.write(self.style.SUCCESS("--> Listening for messages..."))
        try:
            for message in consumer:
                event = message.value
                user_id = event.get("user_id")

                if user_id:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"--> Received user_deleted event for user_id: {user_id}"
                        )
                    )

                    # Delete all todos for this user
                    todos_deleted, _ = Todo.objects.filter(user_id=user_id).delete()

                    self.stdout.write(
                        self.style.SUCCESS(
                            f"--> Deleted {todos_deleted} todos for user_id: {user_id}"
                        )
                    )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"--> An error occurred in the consumer: {e}")
            )
