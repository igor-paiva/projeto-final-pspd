echo "Starting master"
echo ""

docker exec -it spark-master bash spark-3.1.3-bin-hadoop3.2/sbin/start-master.sh

echo "Starting worker 1"
echo ""

docker exec -it spark-worker-1 bash spark-3.1.3-bin-hadoop3.2/sbin/start-worker.sh -m 1G -c 1 spark://spark-master:7077


echo "Starting worker 2"
echo ""

docker exec -it spark-worker-2 bash spark-3.1.3-bin-hadoop3.2/sbin/start-worker.sh -m 1G -c 1 spark://spark-master:7077
