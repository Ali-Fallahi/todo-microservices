#!/bin/sh

# Set the script to exit immediately if a command exits with a non-zero status.
set -e

# Start the Kafka consumer in the background
echo "--> Starting Kafka consumer process in the background..."
python manage.py listen_for_events &

# Start the Django development server in the foreground
# This will be the main process for the container
echo "--> Starting Django server in the foreground..."
exec python manage.py runserver 0.0.0.0:8000