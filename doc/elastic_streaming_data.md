## Elasticsearch

### Docker setup
Use docker-compose to start the Elasticsearch and Kibana containers in
[../elasticsearch/docker](../elasticsearch/docker).

### Setup a data stream
All the steps necessary to create a data stream are in the file [elastic.py](../bibot/elastic.py). The function 

```
setup_data_stream(client)
```
will handle everything automatically.

### Load data into stream
The function
```
start_24h_ticker_stream(symbol, duration, callback)
```
will establish a connection with the binance server and receive messages in real time for current transactions of a symbol. Providing a callback like
```
elastic.message_handler(client, message)
```
will store the message in a running elastic search instance.

### Basic timeseries queries

Use Kibana dev tools to execute the queries. Assuming data has been loaded recently with bibot.
Get the last 20 timeseries records from past hour.
```
GET binance*/_search
{
  "size": 20,
  "query": {
    "range": {
      "@timestamp": {
        "gte": "now-1h"
      }
    }
  }
}
```

Aggregates all timeseries records from the past hour in a 10s interval and assigns each bucket the smallest price.
```
GET binance*/_search 
{ 
  "query": {
    "range": {
      "@timestamp": {
        "gte": "now-1h"
      }
    }
  },
  "size": 0, 
  "aggs": { 
    "binance_histogram": { 
      "date_histogram": { 
        "field": "@timestamp", 
        "fixed_interval": "10s" 
      },
      "aggs": {
        "last_price": {
          "min": {
            "field": "current_price"
          }
        }
      }
    } 
  } 
}
```
### Kibana
Access Kibana by entering
```
http://localhost:5601
```
in your browser.

#### Kibana dashboard
A [dashboard](../elasticsearch/dashboard) can be loaded into Kibana with a [script](../elasticsearch/scripts). Usage:
```shell
./imp_dash.sh [FILENAME]
```