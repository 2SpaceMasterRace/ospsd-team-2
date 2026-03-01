from aws_client_impl.src.s3_client import S3Client
from cloud_storage_client_api.src.client import register_client

def register() -> None:
    """Register the S3 client implementation."""
    register_client(S3Client)

register()