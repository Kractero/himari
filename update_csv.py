import pandas as pd
from datetime import datetime, timedelta, timezone
from urllib.request import urlopen, Request
import json

utc_now = datetime.now(timezone.utc)
previous_utc_day = (utc_now - timedelta(days=1)).strftime("%Y-%m-%d")
api_url = f"https://maki.kractero.com/api/daily?day={previous_utc_day}"
try:
    with urlopen(Request(api_url)) as response:
        if response.status == 200:
            response_data = response.read().decode('utf-8')
            json_data = json.loads(response_data)
            json_df = pd.DataFrame(json_data['trades'])
            csv_df = pd.read_csv('files/trades.csv')
            combined_df = pd.concat([csv_df, json_df], ignore_index=True)

            combined_df.to_csv('files/trades.csv', index=False)

            print("Data successfully appended to trades.csv")
            with open('files/trades.csv', 'r') as file:
                lines = file.readlines()
                print("Last 36 lines of trades.csv:")
                print(''.join(lines[-36:]))
        else:
            print(f'Failed to fetch data from API with status {response.status}')
except Exception as e:
    print(f'An error occurred: {e}')
