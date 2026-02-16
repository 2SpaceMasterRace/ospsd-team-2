from cloud_storage_client_api import CloudStorageClient


class S3Client(CloudStorageClient):
    """AWS S3 implementation of the CloudStorageClient interface."""

    def __init__(self, bucket_name: str, region: str = "us-east-1") -> None:
        self._bucket_name = bucket_name
        self._region = region

    def upload_file(self, local_path: str, remote_path: str) -> str:
        # TODO: Implement with boto3
        raise NotImplementedError

    def download_file(self, remote_path: str, local_path: str) -> None:
        # TODO: Implement with boto3
        raise NotImplementedError

    def list_files(self, prefix: str = "") -> list[str]:
        # TODO: Implement with boto3
        raise NotImplementedError

    def delete_file(self, remote_path: str) -> None:
        # TODO: Implement with boto3
        raise NotImplementedError
