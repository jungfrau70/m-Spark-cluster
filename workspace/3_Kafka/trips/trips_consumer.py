
from kafka import KafkaConsumer 
import json 

brokers = ["kafka1:19091", "kafka2:19092", "kafka3:19093"]
# brokers = ["kafka1:9091", "kafka2:9092", "kafka3:9093"]

topicName = "trips"
consumer = KafkaConsumer(topicName, bootstrap_servers=brokers)

for message in consumer:
  row = json.loads(message.value.decode())
  #print(row)
  
  # processing only if over $10
  if float(row[10]) > 10:
    print(row[10])
