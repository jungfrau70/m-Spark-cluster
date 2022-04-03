
from kafka import KafkaProducer 
import csv 
import json 
import time 

brokers = ["kafka1:19091", "kafka2:19092", "kafka3:19093"]
# brokers = ["kafka1:9091", "kafka2:9092", "kafka3:9093"]

producer = KafkaProducer(bootstrap_servers = brokers)

topicName = "trips"

with open("./trips/yellow_tripdata_2021-01.csv", "r") as file:
  reader = csv.reader(file)
  headings = next(reader)

  for row in reader:
    producer.send(topicName, json.dumps(row).encode("utf-8"))
    print(row)
    time.sleep(1)
