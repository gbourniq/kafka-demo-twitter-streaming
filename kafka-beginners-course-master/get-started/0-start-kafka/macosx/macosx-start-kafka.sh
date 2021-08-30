# cd into kafka folder 
cd kafka_2.13-2.8.0

# make a zookeeper data directory
mkdir data
mkdir data/zookeeper

# Edit config/zookeeper.properties
# change line to 
# dataDir=/Users/guillaume.bournique/kafka_2.13-2.8.0/data/zookeeper

# start zookeeper (make sure nothing is running on port 2181)
zookeeper-server-start config/zookeeper.properties

# Open a new terminal (we leave zookeeper running in previous terminal)

# create Kafka data directory
mkdir data/kafka
# Edit config/server.properties
# change line to 
# log.dirs=/Users/guillaume.bournique/kafka_2.13-2.8.0/data/kafka

# start Kafka
kafka-server-start config/server.properties

# Kafka is running! 
# Keep the two terminal windows opened