import boto3
from botocore.client import Config
from django.conf import settings


def generate_presigned_url(filepath, location = "protected"):
    object_storage_key = f"{location}/{filepath}"
    s3 = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME,
        config=Config(signature_version=settings.AWS_S3_SIGNATURE_NAME)
    )
    print(s3)
    url = s3.generate_presigned_url(
        'get_object',
        Params = {
            'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
            'Key': object_storage_key
        },
        ExpiresIn=3600, # URL ends in 1 hour
    )
    return url