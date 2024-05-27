import time
import requests
import json
from confluent_kafka import Producer, KafkaError
import logging

# Setting up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize Confluent Kafka producer
config = {
    'bootstrap.servers': 'kafka:9092'
}
producer = Producer(**config)

def acked(err, msg):
    if err is not None:
        logging.error("Failed to deliver message: %s: %s", str(msg), str(err))
    else:
        logging.info("Message produced: %s", str(msg))

# List of cryptocurrency pairs to fetch
cryptos = ["XBTUSD", "ETHUSD", "SOLUSD", "INJUSD", "RNDRUSD", "ADAUSD", "LINKUSD", "MATICUSD", "MANAUSD", "AXSUSD", "ENJUSD"]

def fetch_historical_data():
    base_url = "https://api.kraken.com/0/public/OHLC"
    interval = 1440  # Daily data. Adjust as needed (1 = 1 minute, 1440 = 1 day)
    try:
        for crypto in cryptos:
            url = f"{base_url}?pair={crypto}&interval={interval}"
            response = requests.get(url)
            attempt = 0
            while response.status_code != 200 and attempt < 3:
                time.sleep(10)  # wait 10 seconds before retrying
                response = requests.get(url)
                attempt += 1
            if response.status_code == 200:
                data = response.json()
                if 'error' not in data and data['result']:
                    for entry in data['result'][crypto]:
                        simplified_data = {
                            'time': entry[0],
                            'open': entry[1],
                            'high': entry[2],
                            'low': entry[3],
                            'close': entry[4],
                            'vwap': entry[5],
                            'volume': entry[6],
                            'count': entry[7]
                        }
                        producer.produce('crypto_topic', json.dumps(simplified_data).encode('utf-8'), callback=acked)
                        logging.info(f"Sent historical data for {crypto}: {simplified_data}")
                        producer.poll(0.1)
                else:
                    logging.error(f"Error fetching historical data for {crypto}: {data.get('error', 'Unknown error')}")
            else:
                logging.error(f"Failed to fetch data for {crypto} after {attempt} attempts")
            time.sleep(1)  # Respect API rate limits
    except Exception as e:
        logging.exception("Failed to fetch or send data due to an exception: %s", e)

if __name__ == "__main__":
    while True:
        fetch_historical_data()
        time.sleep(3600)  # Fetch hourly or adjust to your needs
        producer.flush()  # Ensure all messages are sent before looping
