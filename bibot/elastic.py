POLICY_NAME = "binance-timeseries-policy"
MAPPING_NAME = "binance-timeseries-mapping"
SETTINGS_NAME = "binance-timeseries-settings"
INDEX_TEMPLATE_NAME = "binance-timeseries-index"
INDEX_ALIAS = "binance"

ILM = {
    "phases": {
        "hot": {
            "actions": {
                "rollover": {
                    "max_age": "1d"
                }
            }
        },
        "delete": {
            "min_age": "7d",
            "actions": {
                "delete": {}
            }
        }
    }
}

mapping_template = {
    "mappings": {
        "properties": {
            "@timestamp": {
                "type": "date",
                "format": "date_optional_time||epoch_millis"
            },
            "symbol": {
                "type": "keyword"
            },
            "current_price": {
                "type": "double"
            }
        }
    }
}

settings_template = {
    "settings": {
        "index.lifecycle.name": POLICY_NAME
    }
}


def setup_data_stream(client):
    """
        Executes all steps necessary to create a data stream.
        Argument:
            client: an instance of the Elasticsearch client
    """
    client.ilm.put_lifecycle(name=POLICY_NAME, policy=ILM)
    client.cluster.put_component_template(name=MAPPING_NAME, template=mapping_template)
    client.cluster.put_component_template(name=SETTINGS_NAME, template=settings_template)
    client.indices.put_index_template(name=INDEX_TEMPLATE_NAME, index_patterns=[INDEX_ALIAS + "*"], data_stream={},
                                      priority=500, composed_of=[SETTINGS_NAME, MAPPING_NAME])


def message_handler(client, message):
    if "result" not in message.keys():
        document = {"@timestamp": message.get("E"), "current_price": message.get("c"), "symbol": message.get("s")}
        add_timeseries_data(client, document)


def add_timeseries_data(client, document):
    client.index(index=INDEX_ALIAS, document=document)
