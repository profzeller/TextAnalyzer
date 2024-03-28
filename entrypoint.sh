#!/bin/sh

# Exit if any command fails
set -e

# Run Django database migrations
echo "Making migrations..."
python manage.py makemigrations

echo "Applying migrations..."
python manage.py migrate

# Load initial data
echo "Loading data..."
python manage.py loaddata readability_tests.json

# Start the main process.
exec "$@"
