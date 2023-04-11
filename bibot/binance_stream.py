import json
import time
import dotenv
from binance.websocket.spot.websocket_client import SpotWebsocketClient as Client

dotenv.load_dotenv()


def message_handler(file, message):
    """ Example code:
        f = init_json_array_file("BTCEUR", "stream")
        start_24h_ticker_stream("BTCEUR", 10, lambda m: message_handler(f, m))
    """
    if "result" not in message.keys():
        file.write(json.dumps(message))
        file.write(",")


def start_24h_ticker_stream(symbol, duration, callback):
    """ Subscribe to Binance stream for given Symbol and duration.
        Will disconnect at the 24h mark by binance server.
        Arguments:
            symbol: str -> e.g. "BTCEUR"
            duration: int -> seconds
            callback: function which handles the incoming messages
    """

    client = Client()
    client.start()

    client.ticker(
        symbol=symbol,
        id=1,
        callback=callback,
    )

    time.sleep(duration)

    # connection is closed uncleanly. Seems to be a upstream issue. See https://github.com/binance/binance-connector-python/issues/168
    # probably has no severe negative effect
    client.stop()
