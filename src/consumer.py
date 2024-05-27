import logging
from kafka import KafkaConsumer
import json
import psycopg2

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

consumer = KafkaConsumer(
    'crypto_topic',
    bootstrap_servers=['kafka:9092'],
    auto_offset_reset='earliest',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

conn = psycopg2.connect(host='postgres', dbname='streamingdb', user='user', password='password')
cursor = conn.cursor()

insert_sql = """
INSERT INTO crypto_prices (name, last_trade, volume, time) VALUES (%s, %s, %s, NOW())
"""

def store_data_in_db(data):
    try:
        for crypto, details in data['result'].items():
            last_trade = details['c'][0]  # Last trade price
            volume = details['v'][1]     # Volume
            cursor.execute(insert_sql, (crypto, last_trade, volume))
            conn.commit()
            logging.info(f"Stored data for {crypto}: Last trade: {last_trade}, Volume: {volume}")
    except Exception as e:
        conn.rollback()
        logging.error(f"Failed to store data due to {e}")

if __name__ == "__main__":
    try:
        for message in consumer:
            store_data_in_db(message.value)
    except KeyboardInterrupt:
        logging.info("Stopping consumer...")
    finally:
        cursor.close()
        conn.close()
        logging.info("Database connection closed.")


