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
# https://faust.readthedocs.io/en/latest/playbooks/vskafka.html
import faust
from typing import List

class Data(faust.Record):
    id: str
    text: str
   
class MatchingRules(faust.Record):
    id: str
    tag: str
 
class Event(faust.Record):
    data: Data
    matching_rules: List[MatchingRules]

app = faust.App(
    'kafka-demo-twitter-faust',
    broker='kafka://localhost:9092',
    value_serializer='json'
)

# source topic
source_topic = app.topic('twitter_tweets', value_type=Event)

# destination topics
dest_topic_cat = app.topic('twitter_tweets_filtered_cat')
dest_topic_dog = app.topic('twitter_tweets_filtered_dog')
dest_topic_dog_parsed = app.topic('twitter_tweets_filtered_dog_parsed')
       
@app.agent(source_topic, sink=[dest_topic_cat])
async def process_cats(stream):
    async for event in stream:
        if "cat" in event.matching_rules[0].tag:
            print(f'Forwarded {event} to topic {dest_topic_cat}')
            yield event

@app.agent(source_topic, sink=[dest_topic_dog])
async def process_dogs(stream):
    async for event in stream:
        if "dog" in event.matching_rules[0].tag:
            print(f'Forwarded {event} to topic {dest_topic_dog}')
            yield event

@app.agent(dest_topic_dog, sink=[dest_topic_dog_parsed])
async def process_dogs_yield_text_only(stream):
    async for event in stream:
        print(f'Forwarded {event} to topic {dest_topic_dog_parsed}')
        yield event.data.text

if __name__ == '__main__':
    app.main()