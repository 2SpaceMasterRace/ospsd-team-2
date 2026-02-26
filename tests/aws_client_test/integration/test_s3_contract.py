import pytest
from cloud_storage_client_api.client import CloudStorageClient
from aws_client_impl.s3_client import S3Client


def test_s3client_is_subclass_of_interface():
    assert issubclass(S3Client, CloudStorageClient)


def test_s3client_can_be_instantiated():
    # This will fail if abstract methods are not correctly implemented
    client = S3Client(bucket_name="dummy")
    assert isinstance(client, CloudStorageClient)