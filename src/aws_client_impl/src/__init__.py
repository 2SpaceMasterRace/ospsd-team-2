"""Public exports for the AWS S3 client implementation package."""
from aws_client_impl.s3_client import S3Client, get_client_impl
from aws_client_impl.s3_client import register as _register_client

def register() -> None:
    """Register the S3 client implementation."""
    _register_client()

register()