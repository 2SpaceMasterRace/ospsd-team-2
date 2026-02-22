"""AWS S3 implementation of the cloud storage client."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import boto3
import structlog
from botocore.exceptions import ClientError

from cloud_storage_client_api import CloudStorageClient

log: Any = structlog.get_logger()
# reference: https://docs.aws.amazon.com/boto3/latest/reference/services/s3/service-resource/create_bucket.html
s3 = boto3.resource("s3")


class S3Client(CloudStorageClient):
    """AWS S3 implementation of the CloudStorageClient interface."""

    def __init__(self, bucket_name: str, region_name: str = "us-east-1") -> None:
        """Initialize the S3 client.

        Args:
            bucket_name: Name of the S3 bucket to work with.
            region_name: AWS region name, defaults to us-east-1.

        """
        self._bucket_name = bucket_name
        self._region_name = region_name

    def create_bucket(
        self, bucket_name: str, region_name: str | None = None,
    ) -> bool:
        """Create an Amazon S3 bucket.

        The name of an Amazon S3 bucket must be unique across
        all regions of the AWS platform. If region is not specified,
        the bucket is created in the S3 default region (us-east-1).

        Args:
            bucket_name: Bucket to create.
            region_name: String region to create a bucket in,
                e.g., ``us-west-2``.

        Returns:
            True if the bucket was created successfully,
            False otherwise.

        Raises:
            ClientError: If the bucket creation fails due to
                AWS service errors (logged and caught).

        """
        if region_name is None:
            region_name = "us-east-1"

        # Note: Consider adding resilience patterns in future iterations
        try:
            bucket_config: dict[str, Any] = {}
            s3_client = boto3.client("s3", region_name)
            log.info("Creating Amazon S3 Bucket...")
            if region_name != "us_east-1":
                bucket_config["CreateBucketConfiguration"] = {
                    "LocationConstraint": region_name,
                }

            s3_client.create_bucket(Bucket=bucket_name, **bucket_config)

        except ClientError:
            log.exception(
                "Failed to create Amazon S3 Bucket",
                bucket_name=bucket_name,
                region_name=region_name,
            )
            return False
        return True

    def upload_file(self, local_path: str, remote_path: str) -> str:
        """Upload a file to S3.

        .. todo:: Implement with boto3.

        """
        raise NotImplementedError

    # Note: ExtraArgs parameter and Callback parameter can be used to implement
    # a progress monitor. Reference for ExtraArgs parameters:
    # https://docs.aws.amazon.com/boto3/latest/reference/
    # customizations/s3.html#boto3.s3.transfer.S3Transfer.ALLOWED_UPLOAD_ARGS
    def download_file(
        self, bucket_name: str, object_name: str, file_name: str,
    ) -> bool:
        """Download an S3 object to a file.

        The ``download_file`` method accepts the names of the bucket
        and object to download and the filename to save the file to.

        Args:
            bucket_name: The name of the bucket to download from.
            object_name: The name of the key to download from.
            file_name: The path to the file to download to.

        Returns:
            True if the file was downloaded successfully,
            False otherwise.

        Raises:
            ClientError: If the download fails due to
                AWS service errors (logged and caught).

        """
        try:
            log.info("Downloading S3 Object to a file...")
            s3.download_file(bucket_name, object_name, file_name)
        except ClientError:
            log.exception(
                "Failed to download file from Amazon S3 Bucket",
                bucket_name=bucket_name,
                object_name=object_name,
                file_name=file_name,
            )
            return False
        return True

    # Note: Consider combining download_file and download_fileobj in the future
    def download_fileobj(
        self,
        bucket_name: str,
        object_name: str,
        file_name: str,
        file_object: str,
    ) -> bool:
        """Download an S3 object to a file-like object.

        The file-like object must be in binary mode. The
        ``download_fileobj`` method is a managed transfer which
        will perform a multipart download in multiple threads
        if necessary.

        Args:
            bucket_name: The name of the bucket to download from.
            object_name: The name of the key to download from.
            file_name: The path to the file to download to.
            file_object: A file-like object to download into.

        Returns:
            True if the file-like object was successfully
            downloaded into, False otherwise.

        Raises:
            ClientError: If the download fails due to
                AWS service errors (logged and caught).

        """
        try:
            log.info("Downloading S3 Object to a file...")
            with Path(file_name).open("wb") as f:
                s3.download_fileobj(bucket_name, object_name, f)

        except ClientError:
            log.exception(
                "Failed to download file from Amazon S3 Bucket",
                bucket_name=bucket_name,
                object_name=object_name,
                file_name=file_name,
                file_object=file_object,
            )
            return False
        return True

    def list_files(self, prefix: str = "") -> list[str]:
        """List files in the S3 bucket.

        .. todo:: Implement with boto3.

        """
        raise NotImplementedError

    # Note: Batch deletion of multiple files could be added for efficiency
    def delete_file(
        self, bucket_name: str, object_name: str,
    ) -> dict[str, Any]:
        """Remove an object from a bucket.

        The behavior depends on the bucket's versioning state:

        - If bucket versioning is not enabled, the operation
          permanently deletes the object.
        - If bucket versioning is enabled, the operation inserts
          a delete marker, which becomes the current version of
          the object. To permanently delete an object in a
          versioned bucket, you must include the object's
          ``versionId`` in the request.

        You can delete objects by explicitly calling DELETE Object
        or calling (PutBucketLifecycle) to enable Amazon S3 to
        remove them for you.

        Args:
            bucket_name: The name of the bucket containing
                the object.
            object_name: The name of object to delete.

        Returns:
            A dict with ``DeleteMarker`` (bool) indicating
            whether the specified object version that was
            permanently deleted was a delete marker before
            deletion.

        Raises:
            ClientError: If the deletion fails due to
                AWS service errors (logged and caught).

        """
        try:
            log.info("Deleting S3 Object...")
            response = s3.delete_project(bucket_name, object_name)
        except ClientError:
            log.exception(
                "Failed to delete object from Amazon S3 Bucket",
                bucket_name=bucket_name,
                object_name=object_name,
            )
            return response
        return response
