from kafka import KafkaConsumer
import json
import time
import requests
import os
from dotenv import load_dotenv

consumer = KafkaConsumer(
    "order-delivery",
    bootstrap_servers="localhost:9092",
    group_id="order-group",
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
)


load_dotenv()

# Access the salt from the environment variables
API = os.environ["MAIL_API"]


def send_email(order_id, email):
    return requests.post(
        "https://api.mailgun.net/v3/sandboxc2b933f32d9d49cf9ec66e2fd96504c2.mailgun.org/messages",
        auth=("api", API),
        data={
            "from": "Excited User <mailgun@sandboxc2b933f32d9d49cf9ec66e2fd96504c2.mailgun.org>",
            "to": email,
            "subject": "Order dispatched",
            "text": f"Your order {order_id} has been dispatched!",
        },
    )


def process_order(order_id, email):
    print(f"Processing order {order_id}: Packing stage...")
    time.sleep(2)
    print(f"Processing order {order_id}: Dispatching stage...")
    time.sleep(2)
    print(
        f"Order {order_id} dispatched! Sending email to the customer with email {email}..."
    )

    send_email(order_id, email)


def process_orders():
    while True:
        messages = consumer.poll(timeout_ms=1000)  # non-blocking
        for tp, batch in messages.items():
            for message in batch:
                order_id = message.value["order_id"]
                status = message.value["status"]
                email = message.value["email"]
                print(order_id, status)
                if status == "paid":
                    process_order(order_id, email)


process_orders()