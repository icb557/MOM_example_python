import pika
from time import sleep

# Retry mechanism for connecting to RabbitMQ
def connect_to_rabbitmq():
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
            print("✅ Connected to RabbitMQ")
            return connection
        except pika.exceptions.AMQPConnectionError as e:
            print(f"❌ Connection failed: {e}, retrying in 5 seconds...")
            sleep(5)

# Connect to RabbitMQ
connection = connect_to_rabbitmq()
channel = connection.channel()

# Declare the fanout exchange (must match the producer)
exchange_name = 'orders_exchange'
channel.exchange_declare(exchange=exchange_name, exchange_type='fanout')

# Create a new, exclusive queue for this consumer
# queue_name = 'shipping'
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

# Bind the queue to the exchange
channel.queue_bind(exchange=exchange_name, queue=queue_name)

# Callback to process messages
def callback(ch, method, properties, body):
    print(f"📦 Consumer [{queue_name}] processing: {body.decode()}")
    sleep(10)
    print("🚚 Order shipped")


# Start consuming messages
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
print("🎧 Waiting for orders...")
channel.start_consuming()
