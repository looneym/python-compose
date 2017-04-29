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

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

channel.basic_consume(callback,
                      queue='hello',
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
