#################################
#### DOWNLOAD KAFKA BINARIES ####
#################################

# Download Kafka at https://kafka.apache.org/quickstart

# Extract Kafka
tar -xvf kafka_2.12-2.0.0.tgz

# Open the Kafka directory
cd kafka_2.12-2.0.0

# Try brew
brew

# Install brew if needed:
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

# Install Java 8 if needed
brew tap homebrew/cask-versions
brew install homebrew/cask-versions/adoptopenjdk8

# Verify Java 8
JAVA_HOME='/Library/Java/JavaVirtualMachines/adoptopenjdk-8.jdk/Contents/Home'
export PATH=$JAVA_HOME/bin:$PATH
java -version

# Try out a Kafka command
bin/kafka-topics.sh

# Install kafka using brew
brew install kafka

# Open a new terminal
# Try a kafka command:
kafka-topics