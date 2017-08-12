# the-prime-directive
An example app for a distributed system built with docker-compose, rabbitMQ and Python asyncio

The system has three main components:

- Sender nodes which produce random numbers and chuck them on a queue
- Worker nodes which consume from the queue and determine if a number is prime
- A web application using Python's async features which reads the primes and displays them to the user

The components communicate over RabbitMQ and Redis and the entire system is orchestrated using docker-compose

This obvioudly has no real-world use but building it was useful for learning about the constraints and design requiements of 
building distributed systems in the real world. For example building logic into the sender and worker nodes to prevent them crashing
should they boot before the message bus is available to connect to.
