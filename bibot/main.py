from elasticsearch import Elasticsearch
import elastic
import binance_stream
import utils as u
import binance_history
import sqlite_historic
import time

# Show elasticsearch
# client = Elasticsearch(hosts="http://@localhost:9200")  # get url/port from .env
#
# elastic.setup_data_stream(client)
#
# binance_stream.start_24h_ticker_stream("BTCEUR", 1000, lambda m: elastic.message_handler(client, m))

# Show sqlite
sqlite_historic.setup_sql_tables()

start_time = time.time()
binance_history.get_agg_trades_since("BTCEUR", "2023-01-16", lambda m: sqlite_historic.insert_data(m, "BTCEUR"))
duration = time.time() - start_time
print(f"total: {duration:.2f} seconds")

data = sqlite_historic.select_all_data()
print(data[:5])

