import boto3
import json
import logging

# Set up professional logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client('s3')

def lambda_handler(event, context):
    """
    AWS Lambda function to automatically remediate public S3 buckets.
    Triggered by EventBridge via CloudTrail API calls.
    """
    try:
        # Extract the bucket name from the CloudTrail event details
        bucket_name = event['detail']['requestParameters']['bucketName']
        logger.info(f"SECURITY ALERT: Public access change detected for bucket: {bucket_name}")

        # Enforce 'Block Public Access' settings immediately
        s3.put_public_access_block(
            Bucket=bucket_name,
            PublicAccessBlockConfiguration={
                'BlockPublicAcls': True,
                'IgnorePublicAcls': True,
                'BlockPublicPolicy': True,
                'RestrictPublicBuckets': True
            }
        )

        logger.info(f"REMEDIATION SUCCESSFUL: Public access for '{bucket_name}' has been restricted.")

        return {
            'statusCode': 200,
            'body': json.dumps({
                'status': 'success',
                'remediated_bucket': bucket_name
            })
        }

    except Exception as e:
        logger.error(f"REMEDIATION FAILED: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'status': 'error',
                'message': 'Internal remediation error'
            })
        }
