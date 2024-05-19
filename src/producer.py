import time
import requests
import json
from confluent_kafka import Producer, KafkaError

# Initialize Confluent Kafka producer
config = {
    'bootstrap.servers': 'kafka:9092'
}
producer = Producer(**config)

def acked(err, msg):
    if err is not None:
        print("Failed to deliver message: %s: %s" % (str(msg), str(err)))
    else:
        print("Message produced: %s" % (str(msg)))

# List of cryptocurrency pairs to fetch
cryptos = ["XBTUSD", "ETHUSD", "SOLUSD", "INJUSD", "RNDRUSD", "ADAUSD", "LINKUSD", "MATICUSD", "MANAUSD", "AXSUSD", "ENJUSD"]

def fetch_crypto_data():
    url = "https://api.kraken.com/0/public/Ticker"
    try:
        for crypto in cryptos:
            response = requests.get(f"{url}?pair={crypto}")
            data = response.json()
            # Serialize data as JSON and encode to utf-8 for the producer
            producer.produce('crypto_topic', json.dumps(data).encode('utf-8'), callback=acked)
            print(f"Sent data for {crypto}: {data}")
            # Wait up to 1 second for events. Callbacks will be invoked during
            # this method call if the message is acknowledged.
            producer.poll(1)
            time.sleep(1)  # Sleep to respect rate limits and reduce load
    except Exception as e:
        print(f"Failed to fetch or send data due to {e}")

if __name__ == "__main__":
    while True:
        fetch_crypto_data()
        time.sleep(300)  # Fetch every 5 minutes
        producer.flush()  # Ensure all messages are sent before looping
