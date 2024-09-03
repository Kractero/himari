import pandas as pd
import sqlite3
from datetime import datetime, timedelta

con = sqlite3.connect("trades.db")
cur = con.cursor()

def get_trade_data_for_date(date_str):
    query = f"""
    SELECT
        DATE(DATETIME(timestamp, 'unixepoch')) AS trade_day,
        season,
        category,
        COUNT(*) AS total_trades,
        SUM(price) AS total_price,
        COUNT(DISTINCT buyer) AS total_buyers,
        COUNT(DISTINCT seller) AS total_sellers,
        SUM(CASE WHEN price = 0 THEN 1 ELSE 0 END) AS total_gifts
    FROM
        trades
    WHERE
        DATE(DATETIME(timestamp, 'unixepoch')) = '{date_str}'
    GROUP BY
        trade_day,
        season,
        category
    """
    return pd.read_sql_query(query, con)

cur.execute("SELECT DATE(MIN(timestamp), 'unixepoch') FROM trades")
earliest_date_str = cur.fetchone()[0]
earliest_date = datetime.strptime(earliest_date_str, "%Y-%m-%d")

end_date = datetime.strptime("2024-09-01", "%Y-%m-%d")

all_data = pd.DataFrame()

current_date = earliest_date
while current_date <= end_date:
    date_str = current_date.strftime("%Y-%m-%d")
    daily_data = get_trade_data_for_date(date_str)
    all_data = pd.concat([all_data, daily_data], ignore_index=True)
    current_date += timedelta(days=1)

all_data.to_csv("trades.csv", index=False)

con.close()
