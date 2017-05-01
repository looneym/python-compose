import pika
import time
from random import randint

connected = False
counter = 1
while not connected:
    try:
        print("Attempring to connect to RabbitMQ. Attempt number %d") % (counter)
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbit'))
        connected = True
    except Exception, e:
        print(str(e))
        print("Unable to establish a connection. Trying again in 45 seconds")
        time.sleep(45)
        counter += 1 

    
channel = connection.channel()
channel.queue_declare(queue='my_queue')

while True:
    x = randint(0,10000)
    channel.basic_publish(exchange='',
                        routing_key='hello',
                        body=str(x))
    print(" [x] Sent %d") % (x)

connection.close()

