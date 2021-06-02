#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z postgres 8090; do
  sleep 0.1
done

echo "PostgreSQL started"

gunicorn -b 0.0.0.0:8080 manage:app
