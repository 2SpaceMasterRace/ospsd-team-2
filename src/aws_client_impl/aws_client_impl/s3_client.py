from cloud_storage_client_api import CloudStorageClient
import boto3
from botocore.exceptions import ClientError
import os

def _get_session() -> boto3.Session:
    """Helper function to create a boto3 session using environment variables."""
    return boto3.Session(region_name=os.environ["AWS_REGION"])

class S3Client(CloudStorageClient):
    """AWS S3 implementation of the CloudStorageClient interface."""

    def __init__(self, bucket_name: str, region: str = "us-east-1") -> None:
        self._bucket_name = bucket_name
        self._region = region
        session = _get_session()
        self._client = session.client("s3")
    

    def upload_file(self, local_path: str, remote_path: str) -> str:
        """Upload a file to an S3 bucket.

        The ``upload_file`` method accepts a local file path and the
        destination object key to upload the file to.

        Args:
            local_path: The path to the local file to upload.
            remote_path: The S3 object key to upload the file to.

        Returns:
            The remote path of the uploaded object.

        Raises:
            ClientError: If the upload fails due to
                AWS service errors (logged and caught).
        """

        try:
            #{logger}
            self._client.upload_file(local_path, self._bucket_name, remote_path)
        except ClientError:
            #{logger}
            raise
        return remote_path

    def download_file(self, remote_path: str, local_path: str) -> None:
        # TODO: Implement with boto3
        raise NotImplementedError

    def list_files(self, prefix: str = "") -> list[str]:
        # TODO: Implement with boto3
        raise NotImplementedError

    def delete_file(self, remote_path: str) -> None:
        # TODO: Implement with boto3
        raise NotImplementedError
