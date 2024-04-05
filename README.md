## SQS Image Processor

SQS Image Processor is a Python application that listens to an Amazon SQS queue for messages containing JSON payloads specifying image URLs. Upon receiving a message, the application downloads the image from the URL, resizes it, and stores both the original and resized versions locally.

## Features

* Receives messages from an Amazon SQS queue.
* Downloads images specified in the message payloads.
* Resizes images to ensure the largest edge is 256px.
* Stores original and resized images in separate directories.
* Handles errors gracefully and retries processing for failed messages.
* Supports custom AWS configurations via environment variables.


## Prerequisites

* Python 3.8 or newer
* Required Python packages (install via pip install -r requirements.txt):
    * requests
    * Pillow
    * boto3 (if not using the sample payload for testing)

## Installation

```bash
    git clone https://github.com/Raam124/sqs_image_processor.git
```

```bash
    pip install -r requirements.txt
```

## Configuration

The application requires the following environment variables to be set:

* AWS_REGION: AWS region where the SQS queue is located.
* AWS_ACCESS_KEY_ID: AWS access key ID for accessing SQS.
* AWS_SECRET_ACCESS_KEY: AWS secret access key for accessing SQS.
* QUEUE_NAME: Name of the SQS queue to listen to.
* DEAD_LETTER_QUEUE_NAME: Name of the dead letter queue for failed messages.

## Usage

Set the required environment variables or test the local way with sample payload.

## Run the application:

```bash
    python sqs_image_processor.py
```

* The application will continuously listen for messages on the specified SQS queue and process them accordingly.


## Important Notes

* SQS-related code parts are commented out for local testing. The application is tested with a default sample payload.
* This script uses an infinite loop for testing purposes. For a production environment, consider implementing a periodic task using Celery to periodically check messages stored in SQS with a broker.
* Here the folders are already created and the sample image is processed so delete both originals and resized folder and run the application for testing or just use a different image url or different sample payload
* The entire application is fully tested locally. Application is not tested using a realtime SQS message queue but the implemention are there according to the boto3 documentation.