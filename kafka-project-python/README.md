# Twitter feeds data pipeline 

Twitter streaming data -> `twitter_tweets` topic -> faust application (filter tweets) -> `twitter_tweets_processed` topic

1. Create a Twitter developer account and set the `TWITTER_BEARER_TOKEN` environment variable.

2. Create topics
```
kafka-topics --bootstrap-server localhost:9092 --topic twitter_tweets --create --partitions 3 --replication-factor 1
kafka-topics --bootstrap-server localhost:9092 --topic twitter_tweets_filtered_cat --create --partitions 3 --replication-factor 1
kafka-topics --bootstrap-server localhost:9092 --topic twitter_tweets_filtered_dog --create --partitions 3 --replication-factor 1
kafka-topics --bootstrap-server localhost:9092 --topic twitter_tweets_filtered_dog_parsed --create --partitions 3 --replication-factor 1
```

3. Start producing tweets: `python kafka_producer_twitter.py` into `twitter_tweets`

4. Start the faust streaming app: `python -m faust -A kafka_streams_filter_tweets worker -l info`. This will take the `twitter_tweets` and redirect records to either the `twitter_tweets_filtered_cat` or `twitter_tweets_filtered_dog` topics. The `twitter_tweets_filtered_dog` topic will be further processed and results loaded to the `twitter_tweets_filtered_dog_parsed` topic.

5. Start the consumer: `python kafka_consumer_console.py` which consumes stream records from `twitter_tweets_filtered_dog_parsed`.


>> Topics can be monitored with a GUI tool like Conduktor.


Useful commands
```
kafka-topics --bootstrap-server localhost:9092 --list
kafka-topics --bootstrap-server localhost:9092 --topic twitter_tweets --describe
kafka-topics --bootstrap-server localhost:9092 --topic twitter_tweets --delete 


# Reset offsets for a consumer group
kafka-consumer-groups --bootstrap-server localhost:9092 --group kafka-demo-twitter-streams --reset-offsets --to-earliest --execute --topic twitter_tweets

kafka-consumer-groups --bootstrap-server localhost:9092 --describe --group kafka-demo-twitter-streams

```