
## Prerequisites

* Python 3.8 or newer
* Required Python packages (install via pip install -r requirements.txt):
    * requests
    * Pillow
    * boto3 (if not using the sample payload for testing)

## Installation

```bash
    git clone https://github.com/your_username/sqs-image-processor.git
```

```bash
    cd sqs-image-processor
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

* Make sure the IAM user associated with the provided access keys has necessary permissions to access SQS and perform required operations.
* Ensure that the AWS credentials are properly configured and accessible from the environment where the application is running.
* SQS-related code parts are commented out for local testing. The application is tested with a default sample payload.
* This script uses an infinite loop for testing purposes. For a production environment, consider implementing a periodic task using Celery to periodically check messages stored in SQS with a broker.
* Here the folders are already created and the sample image is processed delete both originals and resized folder and run the application for testing or just use a diffrent image url or sample payload 