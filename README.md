# Streaming 06: Smart BBQ Smoker Temperature Monitoring System
Publisher: Malcolm Phillip
Date:  29 September 2023

## Overview
This project comprises a temperature monitoring system for three different locations: a smoker, Food A stall, and Food B stall. Temperature data is read from a CSV file and sent to RabbitMQ queues for real-time monitoring. The system alerts when significant temperature changes are detected, ensuring food safety and quality control.

## Prerequisites
1. Python: Make sure you have Python installed. You can download it from python.org.
2. RabbitMQ: Install RabbitMQ from the official RabbitMQ website or use a Docker container for easy setup: docker run -d --hostname my-rabbit --name some-rabbit -p 5672:5672 rabbitmq:3


## How to Run the Code
1. Clone the Respository:
git clone [repository_url]
cd Your file name

1. Intall:
    1. Git
    1. Python 3.7+ (3.11+ preferred)
    1. VS Code Editor
    1. VS Code Extension: Python (by Microsoft)
    1. RabbitMQ Server installed and running locally
    1. pika 1.3.2 (or recent)
    1. Logger 
    1. Webbrowser
    1. sys
    1. Time
    1. csv

1. Run Consumers and Producer in addition to Commands:
    1. For Smoker:
        python Consumer_smoker_bbq.py
    1. For Food A:
        python Consumer_A_smoker_bbq.py
    1. For Food B:
        python Consumer_B_smoker_bbq.py
    1. Run Producer: 
        smoker_bbq_producer.py

## How the Project Works
The project utilizes RabbitMQ queues for real-time data processing. The consumers (Consumer_smoker_bbq.py, Consumer_A_smoker_bbq.py, python Consumer_B_smoker_bbq.py) monitor specific queues for temperature data. If a significant temperature change is detected within a specific time window, an alert is triggered. The producer script (smoker_bbq_producer.py) can be used to simulate temperature data generation for testing purposes.

## Screenshots
### Terminal with Producer & Consumers Running
![Alt text](<Screenshot 2023-09-29 at 5.47.59 PM.png>)

### RabbitMQ Admin Console
![Alt text](<Screenshot 2023-09-29 at 5.48.24 PM-1.png>)
#### Note: Interesting part of the RabbitMQ console, notice all the Totals are "0"

## Reference

- [RabbitMQ Tutorial - Work Queues](https://www.rabbitmq.com/tutorials/tutorial-two-python.html)

- See https://github.com/MPhillipS556427/streaming-03-rabbitmq.git and https://github.com/MPhillipS556427/streaming-04-multiple-consumers.git for remedial training exercises to assist prior to executing this project.
