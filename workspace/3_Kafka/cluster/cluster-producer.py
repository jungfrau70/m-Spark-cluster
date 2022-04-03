from kafka import KafkaProducer 

brokers = ["kafka1:19091", "kafka2:19092", "kafka3:19093"]
# brokers = ["kafka1:9091", "kafka2:9092", "kafka3:9093"]

topicName = "3rd-cluster-topic"

producer = KafkaProducer(bootstrap_servers = brokers)

producer.send(topicName, b"Hello cluster world 2") # send message in byte format
producer.flush() # clean up buffer
