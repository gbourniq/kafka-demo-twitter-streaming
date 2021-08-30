# https://developer.twitter.com/en/docs/tutorials/stream-tweets-in-real-time

import json
import os
import sys
import time

import requests
from kafka import KafkaProducer

# To set your enviornment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = os.environ["TWITTER_BEARER_TOKEN"]

# https://kafka-python.readthedocs.io/en/master/apidoc/KafkaProducer.html
producer = KafkaProducer(
    bootstrap_servers="127.0.0.1:9092",
    # how the data should be serialized before sending to the broker
    # Here, we convert the key to bytes and the value to a json file and encode it to utf-8.
    key_serializer=str.encode,
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    # safe producer - no idempotence setting
    acks="all",
    retries=sys.maxsize,
    max_in_flight_requests_per_connection=5,
    # performance - high throughput producer (at the expense of a bit of latency and CPU usage
    compression_type="gzip",  # snappy would need to be installed
    linger_ms=20,
    batch_size=32 * 1024,  # 32 KB batch size
)

topic_name = "twitter_tweets"


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FilteredStreamPython"
    return r


def get_rules():
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream/rules", auth=bearer_oauth
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot get rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json()))
    return response.json()


def delete_all_rules(rules):
    if rules is None or "data" not in rules:
        return None

    ids = list(map(lambda rule: rule["id"], rules["data"]))
    payload = {"delete": {"ids": ids}}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=bearer_oauth,
        json=payload,
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot delete rules (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    print(json.dumps(response.json()))


def set_rules(delete):
    # You can adjust the rules if needed
    sample_rules = [
        {"value": "dog has:images", "tag": "dog pictures"},
        {"value": "cat has:images -grumpy", "tag": "cat pictures"},
    ]
    payload = {"add": sample_rules}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=bearer_oauth,
        json=payload,
    )
    if response.status_code != 201:
        raise Exception(
            "Cannot add rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json()))


def setup():
    rules = get_rules()
    delete = delete_all_rules(rules)
    set = set_rules(delete)


def get_stream():
    """Twitter API will returns the following schema
    {
        "data": {
            "id": "1431750072362942466",
            "text": "RT @cat_in_a_cage: blah"
        },
        "matching_rules": [
            {
                "id": 1431749862228430848,
                "tag": "cat pictures"
            }
        ]
    }
    """
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream",
        auth=bearer_oauth,
        stream=True,
    )
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Cannot get stream (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    i = 0
    for response_line in response.iter_lines():
        if response_line:
            json_response = json.loads(response_line)
            try:
                producer.send(topic_name, key=json_response['matching_rules'][0]['tag'], value=json_response)
            except Exception as e:
                print(f"Bad data {json.dumps(json_response, indent=4, sort_keys=True)} - Error: {e}")
            
            if i % 100 == 0:
                print(f"Produced {i} records.")
                # print(f"Producer metrics: {producer.metrics()}")
            i += 1


if __name__ == "__main__":
    setup()
    time.sleep(5)
    get_stream()
