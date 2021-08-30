# Replace "kafka-topics" 
# by "kafka-topics.sh" or "kafka-topics.bat" based on your system # (or bin/kafka-topics.sh or bin\windows\kafka-topics.bat if you didn't setup PATH / Environment variables)

kafka-topics 

kafka-topics --bootstrap-server localhost:9092 --list 

kafka-topics --bootstrap-server localhost:9092 --topic first_topic --create

kafka-topics --bootstrap-server localhost:9092 --topic first_topic --create --partitions 3

kafka-topics --bootstrap-server localhost:9092 --topic first_topic --create --partitions 3 --replication-factor 2

kafka-topics --bootstrap-server localhost:9092 --topic first_topic --create --partitions 3 --replication-factor 1

kafka-topics --bootstrap-server localhost:9092 --list 

kafka-topics --bootstrap-server localhost:9092 --topic first_topic --describe

kafka-topics --bootstrap-server localhost:9092 --topic first_topic --delete