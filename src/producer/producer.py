import pika

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare a fanout exchange (it will route messages to all bound queues)
exchange_name = 'orders_exchange'
channel.exchange_declare(exchange=exchange_name, exchange_type='fanout')

# Send a message to the exchange
mensaje = "Order #12345 - 2 products"
channel.basic_publish(exchange=exchange_name, routing_key='orders', body=mensaje)
print(f"✅ Published Order: {mensaje}")

connection.close()
