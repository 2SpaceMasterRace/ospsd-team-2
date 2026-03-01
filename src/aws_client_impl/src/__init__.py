"""AWS implementation of the cloud storage client API."""

import os

from aws_client_impl.src.s3_client import S3Client as S3Client
from cloud_storage_client_api.src.client import CloudStorageClient, register_client


def _create_s3_client() -> CloudStorageClient:
    """Build an S3Client from environment variables."""
    bucket = os.environ.get("AWS_BUCKET_NAME", "")
    region = os.environ.get("AWS_REGION", "us-east-1")
    return S3Client(bucket_name=bucket, region_name=region)


register_client(_create_s3_client)
