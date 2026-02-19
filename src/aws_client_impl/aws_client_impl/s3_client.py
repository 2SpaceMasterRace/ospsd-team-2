from __future__ import annotations

import boto3
from cloud_storage_client_api import CloudStorageClient


class S3Client(CloudStorageClient):
    """AWS S3 implementation of the CloudStorageClient interface."""

    def __init__(self, bucket_name: str, region: str = "us-east-1") -> None:
        self._bucket_name = bucket_name
        self._region = region
        self._s3 = boto3.client("s3", region_name=region)

    def upload_file(self, local_path: str, remote_path: str) -> str:
        # Upload local file to s3://bucket/remote_path
        self._s3.upload_file(local_path, self._bucket_name, remote_path)
        return f"s3://{self._bucket_name}/{remote_path}"

    def download_file(self, remote_path: str, local_path: str) -> None:
        # Download s3://bucket/remote_path to local_path
        self._s3.download_file(self._bucket_name, remote_path, local_path)

    def list_files(self, prefix: str = "") -> list[str]:
        paginator = self._s3.get_paginator("list_objects_v2")
        keys: list[str] = []

        for page in paginator.paginate(Bucket=self._bucket_name, Prefix=prefix):
            for obj in page.get("Contents", []):
                keys.append(obj["Key"])

        return keys

    def delete_file(self, remote_path: str) -> None:
        self._s3.delete_object(Bucket=self._bucket_name, Key=remote_path)
