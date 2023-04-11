import os
import dotenv
import aiohttp
import asyncio
from binance import __version__
from urllib.parse import urljoin
from urllib import parse
import utils as u

dotenv.load_dotenv()
API_KEY = os.getenv("BINANCE_API_KEY")


def get_agg_trades_since(symbol, date, callback):
    asyncio.run(get_agg_trades_since_(symbol, date, callback))


def build_binance_api_url(resource, params={}):
    base_url = "https://api.binance.com/api/v3/"
    resource_url = urljoin(base_url, resource)
    query_start = "?" if params and params.keys() else ""
    return f"{resource_url}{query_start}{parse.urlencode(params)}"


async def call_endpoint(session, url):
    async with session.get(url) as resp:
        response = await resp.json()
        return response


def message_handler(file, message):
    u.dump_array(message, file, delim=",")


async def get_agg_trades_since_(symbol, since, callback):
    """ Calls aggTrades from Binance for symbol and since. Stores the result with a callback.
    Arguments:
        symbol: str -> left hand side is base E.g. BTC and right hand side is quote E.g. EUR
        since: str -> date as a iso string. E.g. 2022-12-01
        callback: function(m) -> the function which writes the message m to disk/db
    Example use:
        asyncio.run(get_agg_trades_since("BTCEUR", "2022-12-01", lambda m: message_handler(file, m)))
    """
    now_millis = u.time_now_millis()
    since_millis = u.date_to_timestamp_millis(since)

    limit = 1000
    base_params = {"symbol": symbol, "limit": limit}
    resource = "aggTrades"
    agg_id = "a"
    async with aiohttp.ClientSession() as session:
        session.headers.update({
            "Content-Type": "application/json;charset=utf-8",
            "User-Agent": "binance-connector/" + __version__.__version__,
            "X-MBX-APIKEY": API_KEY,
        })

        first_batch_url = \
            build_binance_api_url(resource, {**base_params, "startTime": since_millis})
        last_batch_url = \
            build_binance_api_url(resource, {**base_params, "endTime": now_millis})

        first_batch_result = await call_endpoint(session, first_batch_url)
        last_batch_result = await call_endpoint(session, last_batch_url)
        first_batch_index = int(first_batch_result[-1].get(agg_id))
        last_batch_index = int(last_batch_result[0].get(agg_id))
        callback(first_batch_result)

        tasks = []
        for index in range(first_batch_index + limit, last_batch_index - limit, limit):
            url = build_binance_api_url(resource, {**base_params, "fromId": index})
            # TODO potentially add_done_callback to persist immediately
            tasks.append(asyncio.ensure_future(call_endpoint(session, url)))

        responses = await asyncio.gather(*tasks)
        for response in responses:
            callback(response)

        callback(last_batch_result)
