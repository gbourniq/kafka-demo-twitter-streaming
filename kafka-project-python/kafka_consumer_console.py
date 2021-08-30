"""For a real application we could consume the data from kafka and insert it
for e.g. in Elasticsearch or S3 using a connector"""

from typing import List

from kafka import KafkaConsumer
from kafka.consumer.fetcher import ConsumerRecord, TopicPartition


# join a consumer group for dynamic partition assignment and offset commits
# https://kafka-python.readthedocs.io/en/master/apidoc/KafkaConsumer.html
def create_consumer(topics: List[str]):
    consumer = KafkaConsumer(
        ",".join(topics),
        bootstrap_servers="127.0.0.1:9092",
        group_id="kafka-demo-twitter-streams", # consumer group
        auto_offset_reset="earliest",
        enable_auto_commit=False,  # disable auto commit of offsets
        max_poll_records=50,  # disable auto commit of offsets / max batch size
        # key_serializer=,
        value_deserializer=lambda m: m.decode('utf-8'), # callable that takes a raw message value and returns a deserialized value.
    )
    return consumer


def consume_tweets():
    consumer = create_consumer(["twitter_tweets_filtered_dog_parsed"])

    # for msg in consumer:
    #     print(type(msg)) # ConsumerRecord
    #     print(msg)

    while True:
        records_by_partition: Dict[
            TopicPartition, List[ConsumerRecord]
        ] = consumer.poll(timeout_ms=100)
        for topic_partition, records in records_by_partition.items():
            print(f"Received {len(records)} records for partition {topic_partition}")
            if len(records) > 0:
                for record in records:
                    try:
                        # parse record, process data, load to ext. database, etc.
                        print(
                            f"\ntopic {record.topic} - partition {record.partition}"
                            f" - offset {record.offset}"
                            f"\nkey {record.key} - value {record.value}"
                        )
                    except Exception as e:
                        print(f"Skipping bad data {e}")
        # print("Committing offsets...")
        consumer.commit()

    # close the kafka client gracefully
    consumer.close()


if __name__ == "__main__":
    consume_tweets()
