import boto3, os

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("S3_KEY"),
    aws_secret_access_key=os.getenv("S3_SECRET"),
    region_name=os.getenv("S3_REGION")
)

def upload(bucket, key, data):
    s3.put_object(Bucket=bucket, Key=key, Body=data)
