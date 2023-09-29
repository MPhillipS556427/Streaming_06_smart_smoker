
"""This script is designed to monitor and process temperature readings from a RabbitMQ queue, specifically for 'Food A'. 
The temperature data originates from a CSV file and is sent to a RabbitMQ queue, representing the temperature of the specified food item. 
The script establishes a connection to the RabbitMQ server, consumes temperature messages from the 'Food A' queue, and analyzes these readings to detect significant temperature changes over a specific time window.

Author: Malcolm Phillip
Date: 09/28/2023
"""

import pika
from collections import deque

# RabbitMQ configuration
rabbit_host = 'localhost'
rabbit_port = 5672  
food_a_queue = '02-food-A'

# Constants for food stall alert conditions
FOOD_TIME_WINDOW = 10  # minutes
FOOD_DEQUE_MAX_LENGTH = int(FOOD_TIME_WINDOW * 2)  # Assuming one reading every 0.5 minutes
FOOD_TEMP_CHANGE_THRESHOLD = 1  # degrees F

# Create a deque to store temperature readings for food A
food_a_temperature_deque = deque(maxlen=FOOD_DEQUE_MAX_LENGTH)

def show_food_a_alert(timestamp):
     # Print alert message for Food A stall
    
    print(f"Food A Stall Alert at: {timestamp}")

def food_a_callback(ch, method, properties, body):
    try:
        # Decode the message from bytes to a string
        body_str = body.decode('utf-8')
        timestamp = body_str.split()[1]
        temperature = float(body_str.split(':')[3])

        # Add the temperature reading to the deque
        food_a_temperature_deque.append(temperature)
 
        # Print received temperature data for Food A
        print(f"Received food A temperature: {temperature}°F")

        # Check if the deque has at least 20 readings
        if len(food_a_temperature_deque) >= 20:
            # Initialize a flag to track if the temperature change threshold is met
            threshold_met = False

            # Calculate the temperature change over the last 20 readings
            temp_changes = [food_a_temperature_deque[i] - food_a_temperature_deque[i - 1] for i in range(-1, -20, -1)]

            # Check if any of the temperature changes exceed the threshold
            if any(temp_change > FOOD_TEMP_CHANGE_THRESHOLD for temp_change in temp_changes):
                threshold_met = True

            # If the threshold is met, trigger the alert
            if threshold_met:
                show_food_a_alert(timestamp)

            # Clear the deque every 20 readings
            if len(food_a_temperature_deque) % 20 == 0:
                food_a_temperature_deque.clear()

    except ValueError:
        print("Invalid temperature value in message body.")
    except Exception as e:
        print(f"Error processing message: {str(e)}")


def main():
     # Establish a connection to RabbitMQ server and consume messages for Food A queue
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbit_host, port=rabbit_port))
    channel = connection.channel()
    # Declare the queue and set up the callback function
    channel.queue_declare(queue=food_a_queue, durable=True)
    # Start consuming messages for Food A queue
    channel.basic_consume(queue=food_a_queue, on_message_callback=food_a_callback, auto_ack=True)
    
    # Print a message indicating the consumer is waiting for messages
    # Start consuming messages
    print("Food A Consumer is waiting for messages. To exit, press Ctrl+C")
    channel.start_consuming()

if __name__ == '__main__':
    try:
        # Run the main function to start consuming messages
        main()
    except KeyboardInterrupt:
        # Handle keyboard interrupt to exit the script
        print("\nSafely exiting...")