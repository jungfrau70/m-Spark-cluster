
from kafka import KafkaProducer 
import datetime 
import pytz 
import time 
import random 
import json 


TOPIC_NAME = "payments"
brokers = ["kafka1:19091", "kafka2:19092", "kafka3:19093"]
producer = KafkaProducer(bootstrap_servers=brokers)

def get_time_date():
  utc_now = pytz.utc.localize(datetime.datetime.utcnow())
  kst_now = utc_now.astimezone(pytz.timezone("Asia/Seoul"))
  d = kst_now.strftime("%m/%d/%Y")
  t = kst_now.strftime("%H:%M:%S")
  return d, t 

def generate_payment_data():
  payment_type = random.choice(["VISA", "MASTERCARD", "BITCOIN"])
  amount = random.randint(0, 100)
  to = random.choice(["me", "mom", "dad", "friend", "stranger"])
  return payment_type, amount, to

while True:
  d, t = get_time_date()
  payment_type, amount, to = generate_payment_data() 
  new_data = {
    "DATE": d,
    "TIME": t,
    "PAYMENT_TYPE": payment_type,
    "AMOUNT": amount,
    "TO": to,
  }

  # convert python object to json, and then in utf-8 format
  producer.send(TOPIC_NAME, json.dumps(new_data).encode("utf-8"))

  print(new_data)
  time.sleep(1)
