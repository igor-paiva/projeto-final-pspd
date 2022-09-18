echo "Downloading Spark 3.1.3"
echo ""

wget https://dlcdn.apache.org/spark/spark-3.1.3/spark-3.1.3-bin-hadoop3.2.tgz

tar xzf spark-3.1.3-bin-hadoop3.2.tgz

rm spark-3.1.3-bin-hadoop3.2.tgz

echo "Downloading Kafka 3.2.1"
echo ""

wget https://downloads.apache.org/kafka/3.2.1/kafka_2.13-3.2.1.tgz

tar xzf kafka_2.13-3.2.1.tgz

rm kafka_2.13-3.2.1.tgz

echo "Creating docker network"
echo ""

docker network create pspd-projeto-final || true

echo "Overwriting kafka properties"
echo ""

cp kafka_properties/* kafka_2.13-3.2.1/config/

echo "Initializing containers"
echo ""

docker-compose up -d

sleep 2

echo "Creating kafka 'sentences' topic"
echo ""

# to create "sentences" topic
docker exec -it spark-driver bash kafka_2.13-3.2.1/bin/kafka-topics.sh --create --topic sentences --bootstrap-server kafka-server:9092
