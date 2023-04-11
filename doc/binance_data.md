## Description of raw Binance data

### Aggregated Historic Trades

[Raw historic trade](../sample_data/2022-12-13_14-17-53_BTCEUR_hist.json) data consists of a series of trades. The timestamp of the file name denotes the date of retrieval and the currency pair the Binance symbol for which the data has been collected. A trade
has the following properties:

```json
{
  "a": 95843169,          // Aggregate tradeId
  "p": "16322.51000000",  // Price
  "q": "0.00200000",      // Quantity
  "f": 103735974,         // First tradeId
  "l": 103735974,         // Last tradeId
  "T": 1670889600420,     // Timestamp
  "m": true,              // Was the buyer the maker?
  "M": true               // Was the trade the best price match?
}
```

Interesting features are the price property "p" and the timestamp "T". All other properties are considered superfluous and are dropped.
The specified symbol needs to be added to the data so that it is clear to which it belongs. 

### Streaming Data

[24h ticker streaming data](../sample_data/2022-12-14_12-39-39_BTCEUR_stream.json) contains the last 24h statistics for a single symbol.

```json
{
  "e": "24hrTicker",  // Event type
  "E": 1671017981819, // Event time
  "s": "BTCEUR",      // Symbol
  "p": "0.0015",      // Price change
  "P": "250.00",      // Price change percent
  "w": "0.0018",      // Weighted average price
  "x": "0.0009",      // First trade(F)-1 price (first trade before the 24hr rolling window)
  "c": "0.0025",      // Last price
  "Q": "10",          // Last quantity
  "b": "0.0024",      // Best bid price
  "B": "10",          // Best bid quantity
  "a": "0.0026",      // Best ask price
  "A": "100",         // Best ask quantity
  "o": "0.0010",      // Open price
  "h": "0.0025",      // High price
  "l": "0.0010",      // Low price
  "v": "10000",       // Total traded base asset volume
  "q": "18",          // Total traded quote asset volume
  "O": 0,             // Statistics open time
  "C": 86400000,      // Statistics close time
  "F": 0,             // First trade ID
  "L": 18150,         // Last trade Id
  "n": 18151          // Total number of trades
}
```
Interesting properties are all regarding the price and the event time which servers as a timestamp. The symbol is already included.
All other properties can be dropped.