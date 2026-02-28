"""Integration tests for S3Client conformance to CloudStorageClient interface."""

from aws_client_impl.s3_client import S3Client
from client import CloudStorageClient


def test_s3client_is_subclass_of_interface() -> None:
    """Test that S3Client is a subclass of CloudStorageClient."""
    assert issubclass(S3Client, CloudStorageClient)


def test_s3client_can_be_instantiated() -> None:
    """Test that S3Client can be instantiated and is a CloudStorageClient instance.

    This will fail if abstract methods are not correctly implemented.
    """
    client = S3Client(bucket_name="dummy")
    assert isinstance(client, CloudStorageClient)
