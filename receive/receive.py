import pika
import time
import redis

r = redis.Redis(host="redis")
connected = False
counter = 1

def n_prime(a):
    return all(a % i for i in range(2, a))

while not connected:
    try:
        print("Attempring to connect to RabbitMQ. Attempt number %d") % (counter)
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbit'))
        connected = True
    except Exception, e:
        print(str(e))
        print("Unable to establish a connection. Trying again in 30 seconds")
        time.sleep(30)
        counter += 1 

    
channel = connection.channel()
channel.queue_declare(queue='hello')

def callback(ch, method, properties, body):
    p = n_prime(int(body))
    if p:
        r.publish('news', "{}".format(str(body)))
    print(" [x] Received %r" % body)

channel.basic_consume(callback,
                      queue='hello',
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
