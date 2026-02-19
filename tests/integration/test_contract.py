import pytest
from cloud_storage_client_api import CloudStorageClient
from aws_client_impl.s3_client import S3Client

@pytest.mark.integration
def test_s3client_implements_interface():
    c = S3Client(bucket_name="dummy-bucket")
    assert isinstance(c, CloudStorageClient)
