import os
import json
import requests
from PIL import Image
from io import BytesIO
import logging
import signal
import sys
import time

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Directories
ORIGINALS_DIR = 'originals'
RESIZED_DIR = 'resized'

# Sample JSON payload for testing
SAMPLE_JSON_PAYLOAD = {
    "id": "f06795dc-af86-48fe-af5d-b2b35a01fa15",
    "image_url": "https://roccofridge.com/cdn/shop/files/press_module_large.jpg"
}

# AWS configuration (commented out for local testing)
"""
AWS_REGION = os.getenv('AWS_REGION', 'aws_region')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', 'access_key_id')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', 'secret_access_key')
QUEUE_NAME = os.getenv('QUEUE_NAME', 'queue_name')
DEAD_LETTER_QUEUE_NAME = os.getenv('DEAD_LETTER_QUEUE_NAME', 'dead_letter_queue_name')
"""

# SQS client (commented out for local testing)
"""
import boto3

sqs_client = boto3.client('sqs', region_name=AWS_REGION, aws_access_key_id=AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
"""

def download_image(image_url, file_name):
    try:
        response = requests.get(image_url)
        if response.status_code == 200:
            with open(file_name, 'wb') as f:
                f.write(response.content)
            return True
        else:
            logger.error(f"Failed to download image: {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"Error downloading image: {str(e)}")
        return False


def resize_image(image_path, output_path, max_size=256):
    try:
        with Image.open(image_path) as img:
            img.thumbnail((max_size, max_size))
            img.save(output_path)
        return True
    except Exception as e:
        logger.error(f"Error resizing image: {str(e)}")
        return False


def process_message(message, receive_count=0):
    try:
        body = SAMPLE_JSON_PAYLOAD  # Use sample JSON payload for local testing
        message_id = body['id']
        image_url = body.get('image_url')

        # Download original image
        response = requests.head(image_url)
        if 'Content-Type' in response.headers:
            content_type = response.headers['Content-Type']
            if 'image' in content_type:
                extension = content_type.split('/')[-1]
                original_file_name = os.path.join(ORIGINALS_DIR, f"{message_id}.{extension}")
                download_success = download_image(image_url, original_file_name)

                if download_success:
                    # Resize image
                    resized_file_name = os.path.join(RESIZED_DIR, f"{message_id}.{extension}")
                    resize_success = resize_image(original_file_name, resized_file_name)

                    if resize_success:
                        logger.info(f"Image resized and stored: {message_id}")
                    else:
                        logger.error(f"Error resizing image: {message_id}")
                else:
                    logger.error(f"Error downloading image: {message_id}")
            else:
                logger.error(f"URL does not point to an image: {image_url}")
        else:
            logger.error(f"Content-Type header not found in the response for URL: {image_url}")

    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")

        # If processing fails, check the receive count
        if receive_count > 10:
            logger.error(f"Message failed more than 10 times. Sending to dead letter queue: {message}")
            # Uncomment below for AWS SQS integration
            # sqs_client.send_message(QueueUrl=DEAD_LETTER_QUEUE_URL, MessageBody=json.dumps(message))
        else:
            logger.error(f"Reprocessing message: {message}")
            # Uncomment below for AWS SQS integration
            # sqs_client.change_message_visibility(QueueUrl=QUEUE_URL, ReceiptHandle=message['ReceiptHandle'], VisibilityTimeout=0)


def receive_messages():
    while True:
        try:
            # Local testing does not need SQS configuration

            # Uncomment the code below for AWS SQS integration
            """
            queue_url = sqs_client.get_queue_url(QueueName=QUEUE_NAME)['QueueUrl']
            dead_letter_queue_url = sqs_client.get_queue_url(QueueName=DEAD_LETTER_QUEUE_NAME)['QueueUrl']

            response = sqs_client.receive_message(
                QueueUrl=queue_url,
                MaxNumberOfMessages=1,
                WaitTimeSeconds=20
            )

            if 'Messages' in response:
                for message in response['Messages']:
                    receive_count = int(message['Attributes']['ApproximateReceiveCount'])
                    process_message(message, receive_count)
                    sqs_client.delete_message(QueueUrl=queue_url, ReceiptHandle=message['ReceiptHandle'])
            else:
                logger.info("No messages in the queue.")
            """
            # Process sample JSON payload
            process_message(None)

        except Exception as e:
            logger.error(f"Error receiving messages: {str(e)}")

        # Wait for a short period before polling again
        time.sleep(1)


def signal_handler(sig, frame):
    logger.info("Exiting...")
    sys.exit(0)


if __name__ == "__main__":
    # Set up signal handler for graceful termination
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Create directories if they don't exist
    if not os.path.exists(ORIGINALS_DIR):
        os.makedirs(ORIGINALS_DIR)
    if not os.path.exists(RESIZED_DIR):
        os.makedirs(RESIZED_DIR)

    # Start receiving messages
    receive_messages()