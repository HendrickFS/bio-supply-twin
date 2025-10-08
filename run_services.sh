#!/bin/bash
# run_services.sh - Run Django server and MQTT consumer together

echo "Starting Django server and MQTT consumer..."

# Start Django server in background
python manage.py runserver &
DJANGO_PID=$!

# Start MQTT consumer in background  
python manage.py mqtt_consumer &
CONSUMER_PID=$!

echo "Django server running (PID: $DJANGO_PID)"
echo "MQTT consumer running (PID: $CONSUMER_PID)"
echo "Press Ctrl+C to stop both services"

# Function to cleanup processes
cleanup() {
    echo "Stopping services..."
    kill $DJANGO_PID 2>/dev/null
    kill $CONSUMER_PID 2>/dev/null
    exit
}

# Handle Ctrl+C
trap cleanup SIGINT

# Wait for processes
wait