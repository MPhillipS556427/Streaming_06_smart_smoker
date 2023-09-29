"""This script reads temperature data from a CSV file and sends it to RabbitMQ queues.
It also opens the RabbitMQ Admin website for monitoring.
The CSV file contains temperature readings for a smoker and two foods.

Author: Malcolm Phillip
Date: 09/20/2023
"""

import csv
import pika
import time
import webbrowser
import logging

# RabbitMQ configuration
rabbit_host = 'localhost'
rabbit_port = 15672

show_offer = True

queues = {
    '01-smoker': 'Channel1',
    '02-food-A': 'Channel2',
    '03-food-B': 'Channel3'
}

# Configure logging
logging.basicConfig(filename='Smart_BBQ_Smoker.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def offer_rabbitmq_admin_site(host, port):
    """
    Open the RabbitMQ Admin website without asking
    Parameters:
        host (str): this is the localhost
        port (int): this is RabbitMQ UI default port
    """
    global show_offer
    if show_offer:
        url = f"http://{host}:{port}/#/queues"
        webbrowser.open_new(url)
        logging.info("Opened RabbitMQ Admin website.")

def send_temperature_to_queue(time_stamp, temperature, queue_name):
    """
    This function establishes a connection to a RabbitMQ server, declares a durable queue
    with the specified name, creates a message containing the temperature data and timestamp, 
    and sends the message to the specified queue. The message is marked as persistent to ensure it
    survives server failures or restarts.

    Parameters:
        time_stamp (str): The timestamp of temperature reading.
        temperature (float): The temperature value to be sent.
        queue_name (str): The name of the RabbitMQ queue to send the temperature reading to.
    """
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbit_host))
        channel = connection.channel()
        channel.queue_declare(queue=queue_name, durable=True)

        message = f"{time_stamp}: {temperature}"

        channel.basic_publish(exchange='', routing_key=queue_name, body=message, properties=pika.BasicProperties(
            delivery_mode=2,  # Make the message persistent
        ))

        logging.info(f"Sent temperature reading at {time_stamp}, {temperature} to '{queue_name}'")
        connection.close()
    except Exception as e:
        logging.error(f"Error sending temperature to '{queue_name}': {str(e)}")

if __name__ == '__main__':
    try:
        # Open RabbitMQ Admin site
        offer_rabbitmq_admin_site(rabbit_host, rabbit_port)

        # Read temperature data from CSV file and send to RabbitMQ
        csv_file_name = 'smoker-temps.csv'
        sleep_interval = 30  # Sleep for 30 seconds (half a minute)

        with open(csv_file_name, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            data_found = False

            for row in csv_reader:
                time_stamp = row.get('Time (UTC)', '')
                for queue_name, channel_name in queues.items():
                    try:
                        temperature_str = row.get(channel_name, '')
                        if temperature_str:
                            temperature = float(temperature_str)
                            send_temperature_to_queue(time_stamp, temperature, queue_name)
                            data_found = True
                        else:
                            logging.warning(f"Missing temperature value in '{channel_name}' column.")
                    except ValueError:
                        logging.error(f"Invalid temperature value in '{channel_name}' column.")
                    except KeyError:
                        logging.error(f"Invalid column name: '{channel_name}'")

                time.sleep(sleep_interval)
            
            if not data_found:
                logging.warning("No valid data was found in the CSV file.")
    except KeyboardInterrupt:
        logging.info("Safely exiting...")