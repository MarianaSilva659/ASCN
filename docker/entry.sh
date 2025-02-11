#!/bin/sh

echo "DB_HOST=${DB_HOST}" > .env
echo "DB_USER=${DB_USER}" >> .env
echo "DB_PASSWORD=${DB_PASSWORD}" >> .env
echo "DB_NAME=${DB_NAME}" >> .env
echo "DB_PORT=${DB_PORT}" >> .env

# Run migrations if MIGRATE_DB is set to true
if [ "$MIGRATE_DB" = "true" ]; then
    echo "Running database migrations..."
    python3 manage.py migrate
fi

# Seed the database if SEED_DB is set to true
if [ "$SEED_DB" = "true" ]; then
    echo "Seeding the database..."
    python3 seed.py
fi

# Start the server
exec python3 manage.py runserver 0.0.0.0:8000
