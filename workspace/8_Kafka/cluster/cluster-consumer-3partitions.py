
from kafka import KafkaConsumer 

brokers = ["kafka1:19091", "kafka2:19092", "kafka3:19093"]
# brokers = ["kafka1:9091", "kafka2:9092", "kafka3:9093"]

# consumer works like a python generator
consumer = KafkaConsumer("3rd-cluster-topic", bootstrap_servers=brokers) 

for message in consumer:
  print(message)
