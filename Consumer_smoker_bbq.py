
""""This script acts as a consumer for RabbitMQ, processing temperature data received in real-time from a designated queue named '01-smoker'. 
The script continuously listens for messages containing temperature readings. 
If the temperature in the smoker experiences a significant drop exceeding 15°F within a 2.5-minute window (based on the last 5 readings), it triggers a smoker alert. 
When a message is received, it decodes the data and calculates the temperature change over the last 5 readings. 
If any of these changes exceed the specified threshold, a timestamped alert message is printed indicating a potential issue with the smoker's temperature. The script clears the temperature readings every 5 received messages to ensure continuous monitoring.

Author: Malcolm Phillip
Date: 09/28/2023
"""

import pika
import time
from collections import deque

# RabbitMQ configuration
rabbit_host = 'localhost'
rabbit_port = 5672  
smoker_queue = '01-smoker'

# Constants for smoker alert conditions
SMOKER_TIME_WINDOW = 2.5  # minutes
SMOKER_DEQUE_MAX_LENGTH = int(SMOKER_TIME_WINDOW * 2)  # Assuming one reading every 0.5 minutes
SMOKER_TEMP_CHANGE_THRESHOLD = 15  # degrees F

# Create a deque to store temperature readings for the smoker
smoker_temperature_deque = deque(maxlen=SMOKER_DEQUE_MAX_LENGTH)

# Function to show an alert for the smoker when triggered
def show_smoker_alert(timestamp):
    print(f"Smoker Alert at: {timestamp}")

# Callback function for processing messages from the smoker queue
def smoker_callback(ch, method, properties, body):
    try:
        # Decode the message from bytes to a string
        body_str = body.decode('utf-8')
        timestamp = body_str.split()[1]
        temperature = float(body_str.split(':')[3])

        # Add the temperature reading to the deque
        smoker_temperature_deque.append(temperature)

        print(f"Received smoker temperature: {temperature}°F")
    except ValueError:
        print("Invalid temperature value in message body.")
    except Exception as e:
        print(f"Error processing message: {str(e)}")

    # Check if the deque has at least 5 readings
    if len(smoker_temperature_deque) >= 5:
        # Initialize a flag to track if the temperature change threshold is met
        threshold_met = False

        # Calculate the temperature change over the last 5 readings
        temp_changes = [smoker_temperature_deque[i] - smoker_temperature_deque[i - 1] for i in range(-1, -5, -1)]

        # Check if any of the temperature changes exceed the threshold
        if any(temp_change <= -SMOKER_TEMP_CHANGE_THRESHOLD for temp_change in temp_changes):
            threshold_met = True

        # If the threshold is met, trigger the alert
        if threshold_met:
            show_smoker_alert(timestamp)

        # Clear the deque every 5 readings
        if len(smoker_temperature_deque) % 5 == 0:
            smoker_temperature_deque.clear()

# Main function for setting up the RabbitMQ connection and consuming messages
def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbit_host, port=rabbit_port))
    channel = connection.channel()

    # Declare the smoker queue as durable
    channel.queue_declare(queue=smoker_queue, durable=True)

    # Set up the consumer with the callback function
    channel.basic_consume(queue=smoker_queue, on_message_callback=smoker_callback, auto_ack=True)

    # Print a message indicating the consumer is waiting for messages       
    # Start consuming messages
    print("Smoker Consumer is waiting for messages. To exit, press Ctrl+C")
    channel.start_consuming()

# Check if the script is being run directly and start consuming messages
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nSafely exiting...")