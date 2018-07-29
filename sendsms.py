'''
Simple Lambda function that posts to a configured SNS topic
on the click of a button.  It sends different messages based
on a single, double, or long click.

The following JSON template shows what is sent as the payload:
{
    "serialNumber": "GXXXXXXXXXXXXXXXXX",
    "batteryVoltage": "xxmV",
    "clickType": "SINGLE" | "DOUBLE" | "LONG"
}

A "LONG" clickType is sent if the first press lasts longer than 1.5 seconds.
"SINGLE" and "DOUBLE" clickType payloads are sent for short clicks.

For more documentation, follow the link below.
http://docs.aws.amazon.com/iot/latest/developerguide/iot-lambda-rule.html
'''

from __future__ import print_function

import boto3
import json
import logging
import time
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

sns = boto3.client('sns')

def lambda_handler(event, context):
    logger.info('Received event: ' + json.dumps(event))

    # A short press means Ryan is home
    # A double click means Ryan wants Door Dash
    # A long click means call Ryan
    date = time.strftime('%I:%M:%S %p')
    message = 'Ryan is home'
    if (event['clickType'] == 'DOUBLE'):
        message = 'Ryan wants Door Dash'
    elif (event['clickType'] == 'LONG'):
        message = 'Please call Ryan'

    messageObj = {}
    messageObj['default'] = message
    messageObj['email'] = 'A ' + event['clickType'] + ' click was received from IOT device ' + event['serialNumber'] + ' at ' + date + ' UTC'
    messageObj['sms'] = message + ' at ' + date
    sns.publish(TopicArn=os.environ['topic_arn'], Message=json.dumps(messageObj), MessageStructure='json', Subject=message)
    logger.info('Message has been sent to ' + topic_arn)
