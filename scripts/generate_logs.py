import random
import datetime
import json
import os

def generate_log_entry():
    timestamps = [datetime.datetime.now() - datetime.timedelta(minutes=i) for i in range(1000)]
    pages = ["/home", "/about", "/contact", "/products", "/blog"]
    statuses = [200, 404, 500, 301]

    log_entry = {
        "timestamp": random.choice(timestamps).isoformat(),
        "page": random.choice(pages),
        "status": random.choice(statuses),
        "response_time": random.randint(1, 1000)
    }
    return log_entry

if __name__ == "__main__":
    logs = [generate_log_entry() for _ in range(1000)]
    os.makedirs("../data", exist_ok=True)  # Ensure the directory exists
    with open("../data/logs.json", "w") as f:
        json.dump(logs, f, indent=2)
