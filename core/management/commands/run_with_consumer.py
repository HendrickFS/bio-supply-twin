# core/management/commands/run_with_consumer.py
import threading
import subprocess
from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = "Run Django server with MQTT consumer in parallel"

    def handle(self, *args, **options):
        print("Starting Django server with MQTT consumer...")
        
        # Start MQTT consumer in a separate thread
        consumer_thread = threading.Thread(
            target=call_command, 
            args=('mqtt_consumer',),
            kwargs={'broker': 'localhost'}
        )
        consumer_thread.daemon = True
        consumer_thread.start()
        
        print("MQTT consumer started in background")
        print("Starting Django server...")
        
        # Run Django server in main thread
        call_command('runserver')