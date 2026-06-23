import boto3
import os
from botocore.exceptions import ClientError


def get_s3_client():
    return boto3.client('s3', region_name=os.getenv('AWS_REGION'))


def upload_file(file_obj, filename):
    s3 = get_s3_client()
    bucket = os.getenv('S3_BUCKET_NAME')
    s3.upload_fileobj(file_obj, bucket, filename)
    return filename


def generate_download_url(filename, expiry=3600):
    s3 = get_s3_client()
    bucket = os.getenv('S3_BUCKET_NAME')
    url = s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket, 'Key': filename},
        ExpiresIn=expiry
    )
    return url


def delete_file(filename):
    s3 = get_s3_client()
    bucket = os.getenv('S3_BUCKET_NAME')
    s3.delete_object(Bucket=bucket, Key=filename)
