#!/bin/sh

# Wait for Elasticsearch to be available
while ! curl -s http://elasticsearch:9200 >/dev/null; do
  echo "Waiting for Elasticsearch..."
  sleep 5
done

echo "Elasticsearch is up and running"

# Generate logs
python /app/scripts/generate_logs.py

# Run the Python script to ingest logs
python /app/scripts/ingest_to_es.py
