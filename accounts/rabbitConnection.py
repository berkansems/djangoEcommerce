import pika,time
import logging

logger=logging.getLogger("logger2")

class RabbitConnection():

    def __init__(self):
        server_down = True
        while server_down:
            try:
                #the hostname in docker compose file
                #if you wanna run in local you should write 'localhost' in both docker compose and here
                #in local running postgresql data in accounts.settings also should be changed.
                self.initialize_connection(host='rabbithostmq')

                server_down = False
                logger.info('server is up!')

            except:
                server_down = True
                logger.warning('Cannot connect to rabbitmq server.')
                time.sleep(2)


    def initialize_connection(self,host):
        logger.info('Attempting to establish RabbitMQ connection')
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host))
        # Create a new channel with the next available channel number or pass in a channel number to use
        logger.info('connected')

    def write_to_queue(self,message,route):
        channel = self.connection.channel()

        channel.queue_declare(queue='authorized',durable=True)
        channel.queue_declare(queue='notauthorized', durable=True)

        if route==1:
            channel.basic_publish(exchange='authentication',routing_key='permited',body=message)
        elif route==2:
            channel.basic_publish(exchange="authentication",routing_key='notpermited',body=message)
        elif route==3:
            channel.basic_publish(exchange='authentication',routing_key='tosignout',body=message)
        else:
            logger.error("the rout is not defined correctly")