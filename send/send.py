import pika
import time

connected = False
counter = 1
while not connected:
    try:
        print("Attempring to connect to RabbitMQ. Attempt number %d") % (counter)
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbit'))
        print("Connected succesfully")
        connected = True
    except Exception, e:
        print(str(e))
        print("Unable to establish a connection. Trying again in 10 seconds")
        time.sleep(10)
        counter += 1 

    
channel = connection.channel()
channel.queue_declare(queue='hello')

for x in range(0, 100):
  channel.basic_publish(exchange='',
                        routing_key='hello',
                        body=str(x))
  print(" [x] Sent %d") % (x)

connection.close()

