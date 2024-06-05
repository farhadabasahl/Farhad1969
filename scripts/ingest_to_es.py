import json
import requests
import os
import time

ES_HOST = 'http://elasticsearch:9200'
INDEX_NAME = 'web_logs'
LOGS_FILE = '../data/logs.json'

def wait_for_elasticsearch():
    url = f"{ES_HOST}/"
    while True:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print("Elasticsearch is available")
                return True
        except requests.exceptions.ConnectionError:
            print("Waiting for Elasticsearch...")
        time.sleep(5)

def create_index():
    url = f"{ES_HOST}/{INDEX_NAME}"
    headers = {'Content-Type': 'application/json'}
    settings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
        "mappings": {
            "properties": {
                "timestamp": {"type": "date"},
                "page": {"type": "keyword"},
                "status": {"type": "integer"},
                "response_time": {"type": "integer"}
            }
        }
    }
    try:
        response = requests.put(url, headers=headers, data=json.dumps(settings))
        if response.status_code == 200:
            print(f"Index {INDEX_NAME} created successfully")
        elif response.status_code == 400 and 'resource_already_exists_exception' in response.json()['error']['type']:
            print(f"Index {INDEX_NAME} already exists")
        else:
            print(f"Failed to create index {INDEX_NAME}: {response.content}")
    except requests.exceptions.RequestException as e:
        print(f"Error creating index: {e}")

def ingest_logs():
    if not os.path.exists(LOGS_FILE):
        print(f"File {LOGS_FILE} not found. Please ensure the logs.json file exists.")
        return

    try:
        with open(LOGS_FILE, 'r') as f:
            logs = json.load(f)  # Load the entire JSON file as a list of dictionaries

        url = f"{ES_HOST}/{INDEX_NAME}/_bulk"
        headers = {'Content-Type': 'application/json'}
        bulk_data = ""
        for log in logs:
            bulk_data += json.dumps({"index": {}}) + "\n"
            bulk_data += json.dumps(log) + "\n"

        response = requests.post(url, headers=headers, data=bulk_data)
        if response.status_code == 200:
            print("Logs ingested successfully")
        else:
            print(f"Failed to ingest logs: {response.content}")
    except requests.exceptions.RequestException as e:
        print(f"Error ingesting logs: {e}")

if __name__ == "__main__":
    if wait_for_elasticsearch():
        create_index()
        ingest_logs()
