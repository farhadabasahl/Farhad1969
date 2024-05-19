from kafka import KafkaConsumer
import json
import psycopg2

consumer = KafkaConsumer(
    'crypto_topic',
    bootstrap_servers=['kafka:9092'],  # Changed to use Kafka service name
    auto_offset_reset='earliest',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# PostgreSQL connection setup
conn = psycopg2.connect(host='postgres', dbname='streamingdb', user='user', password='password')

 # Adjust as needed
cursor = conn.cursor()

# SQL to insert data
insert_sql = """
INSERT INTO crypto_prices (name, last_trade, volume, time) VALUES (%s, %s, %s, NOW())
"""

def store_data_in_db(data):
    for crypto, details in data['result'].items():
        try:
            last_trade = details['c'][0]  # Last trade price
            volume = details['v'][1]     # Volume
            cursor.execute(insert_sql, (crypto, last_trade, volume))
            conn.commit()
            print(f"Stored data for {crypto}: Last trade: {last_trade}, Volume: {volume}")
        except Exception as e:
            print(f"Failed to store data due to {e}")
            conn.rollback()

if __name__ == "__main__":
    try:
        for message in consumer:
            store_data_in_db(message.value)
    except KeyboardInterrupt:
        print("Stopping consumer...")
    finally:
        cursor.close()
        conn.close()
        print("Database connection closed.")

