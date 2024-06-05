import requests
import pandas as pd
import os

def fetch_kraken_data(pair, start, end):
    url = f'https://api.kraken.com/0/public/OHLC'
    params = {
        'pair': pair,
        'interval': 1440,
        'since': start,
        'end': end
    }
    response = requests.get(url, params=params)
    
    # Print the status code and response for debugging
    print(f"Fetching data for {pair}")
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code == 200:
        try:
            data = response.json()['result'][pair]
            df = pd.DataFrame(data, columns=['time', 'open', 'high', 'low', 'close', 'vwap', 'volume', 'count'])
            return df
        except KeyError as e:
            print(f"KeyError: {e} for pair {pair}")
            print(f"Response JSON: {response.json()}")
            return pd.DataFrame()
    else:
        print(f"Failed to fetch data for {pair}: {response.content}")
        return pd.DataFrame()

pairs = ["XBTUSDC", "XBTUSDT","ETHUSDC", "ETHUSDT", "SOLUSD", "INJUSD", "RNDRUSD", "ADAUSD", "LINKUSD", "MATICUSD", "MANAUSD", "AXSUSD", "ENJUSD"]
start = 1609459200  # Start of 2021
end = 1672444800    # End of 2023

os.makedirs("../data", exist_ok=True)

for pair in pairs:
    df = fetch_kraken_data(pair, start, end)
    if not df.empty:
        df.to_csv(f"../data/{pair}_data.csv", index=False)
    else:
        print(f"No data for {pair}")
