# Replace "kafka-console-consumer" 
# by "kafka-console-consumer.sh" or "kafka-console-consumer.bat" based on your system # (or bin/kafka-console-consumer.sh or bin\windows\kafka-console-consumer.bat if you didn't setup PATH / Environment variables)

# start one consumer
kafka-console-consumer --bootstrap-server 127.0.0.1:9092 --topic first_topic --group my-first-application

# start one producer and start producing
kafka-console-producer --broker-list 127.0.0.1:9092 --topic first_topic

# start another consumer part of the same group. See messages being spread
# messages will be load balanced across consummers part of the same group
# if 3 consumers and 3 partitions, that means each consumers read from 1 partition
kafka-console-consumer --bootstrap-server 127.0.0.1:9092 --topic first_topic --group my-first-application

# starting a second application will not read any existing messages because offsets have been committed in kafka
# start another consumer part of a different group from beginning
kafka-console-consumer --bootstrap-server 127.0.0.1:9092 --topic first_topic --group my-second-application --from-beginning