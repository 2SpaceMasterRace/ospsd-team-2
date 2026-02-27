"""AWS S3 implementation of the cloud storage client."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, BinaryIO

import boto3
import structlog
from botocore.exceptions import ClientError

from cloud_storage_client_api import CloudStorageClient

log: Any = structlog.get_logger()
# reference: https://docs.aws.amazon.com/boto3/latest/reference/services/s3/service-resource/create_bucket.html
s3 = boto3.resource("s3")
log.info("Amazon S3 resource service client initalized")


class S3Client(CloudStorageClient):
    """AWS S3 implementation of the CloudStorageClient interface."""

    def __init__(self, bucket_name: str, region_name: str = "us-east-1") -> None:
        """Initialize the S3 client.

        Args:
            bucket_name: Name of the S3 bucket to work with.
            region_name: AWS region name, defaults to us-east-1.

        """
        self._bucket_name = bucket_name
        self._region = region_name
        session = self._get_session()
        self._client = session.client("s3")

    def upload_file(self, local_path: str, key: str) -> bool:
        """Upload a file to an S3 bucket.

        The ``upload_file`` method accepts a local file path and the
        destination object key to upload the file to.

        Args:
            local_path: The path to the local file to upload.
            key: The S3 object key to upload the file to.

        Returns:
            True, if the upload was successful
            False, if the upload was NOT successful

        Raises:
            ClientError         : If the upload fails due to
                                AWS service errors (logged and caught).
            FileNotFoundError   : If the local_path does not exist.

        """
        if not key:
            log.error("Key cannot be empty")
            raise ValueError
        if key.startswith("/"):
            log.error("S3 object key cannot start with a leading slash")
            raise ValueError
        try:
            log.info("Commencing file upload...")
            self._client.upload_file(local_path, self._bucket_name, key)
            log.info("File Uploaded Sucessfully !")
        except ClientError:
            log.exception("Failed to upload", key=key)
            raise
        except FileNotFoundError:
            log.exception(
                "Unable to locate file. Check file path",
                local_path=local_path)
            raise
        return True

    def upload_obj(self, file_obj: BinaryIO, key: str) -> bool:
        """Upload a file object to an Amazon S3 bucket.

        Args:
            file_obj: A file-like object to upload. Must be opened in binary mode
                or be an in-memory bytes buffer (e.g., ``io.BytesIO``).
            key: S3 object key (the name the file will have in the bucket).

        Returns:
            True if the file was uploaded successfully,
            False otherwise.

        Raises:
            ClientError: If the upload fails due to
                         AWS service errors (logged and caught).

        """
        if not key:
            log.error("Key cannot be empty")
            raise ValueError
        if key.startswith("/"):
            log.error("S3 object key cannot start with a leading slash")
            raise ValueError
        self._validate_file_obj(file_obj=file_obj)
        try:
            log.info("Commencing object upload...")
            self._client.upload_fileobj(file_obj, self._bucket_name, key)
        except ClientError:
            log.exception("Failed to upload", bucket_name=self._bucket_name)
            raise
        return True

    def upload_part(self, body: bytes | BinaryIO, key: str) -> bool:
        """Upload a single part in a multipart upload.

            Must be called after ``create_multipart_upload``
            and before ``complete_multipart_upload`` or ``abort_multipart_upload``.

            Part numbers must be between 1 and 10,000 inclusive and define
            the part's position in the final assembled object. Uploading a
            new part with an already-used part number overwrites the
            previous part.

        Args:
            key     : The S3 object key that was supplied to ``create_multipart_upload``
            body    : The raw bytes or a binary file-like object for this part.
                    All parts except the last must be at least 5 MB.

        Returns:
            True, if the upload was successful
            False, if the upload was NOT sucessful

        Raises:
            ValueError  : If ``key`` is empty, starts with ``'/'``, or
                        ``part_number`` is outside the 1 to 10,000 range.
            ClientError : If the upload fails due to AWS service errors,
                        including ``NoSuchUpload`` (404) when the ``upload_id``
                        is invalid or the multipart upload has already been
                        completed or aborted.

        """
        if not key:
            log.error("Key cannot be empty")
            raise ValueError
        if key.startswith("/"):
            log.error("S3 object key cannot start with a leading slash")
            raise ValueError
        kwargs = {
        "Bucket": self._bucket_name,
        "Key": key,
        "Body": body,
        }
        try:
            log.info(
                "Uploading single part in Multipart upload...",
            )
            self._client.upload_part(**kwargs)
            log.info(
                "SUCESS! Uploaded single part in Multipart upload",
            )
        except ClientError:
            log.exception(
                "Failed to upload part in multipart upload",
                key=key,
                body=body,
            )
            return False
        return True

    def create_bucket(
        self,
        bucket_name: str,
        region_name: str | None = None,
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
            bucket = s3.Bucket(bucket_name)
            if region_name != "us_east-1":
                bucket_config["CreateBucketConfiguration"] = {
                    "LocationConstraint": region_name,
                }
            log.info("Creating Amazon S3 Bucket...")
            s3_client.create_bucket(Bucket=bucket_name, **bucket_config)
            bucket.wait_until_exists()
            log.info(
                "SUCCESS! Created bucket %s in region: %s",
                bucket_name,
                region_name,
            )
        except ClientError:
            log.exception(
                "Failed to create Amazon S3 Bucket",
                bucket_name=bucket_name,
                region_name=region_name,
            )
            return False
        return True

    # There's two methods: delete and delete_bucket which basically do the same thing,
    # don't know how to navigate this
    def delete_bucket(
        self,
        bucket_name: str,
    ) -> bool:
        """Delete an Amazon S3 bucket.

        All objects in the bucket must be deleted
        before the bucket itself can be deleted.

        Args:
             bucket_name: Bucket to delete.

        Returns:
             True if the bucket was deleted successfully,
             False otherwise.

        Raises:
             ClientError: If the bucket deletion fails due to
                 AWS service errors (logged and caught).

        """
        try:
            bucket = s3.Bucket(bucket_name)
            log.info("Deleting Amazon S3 Bucket...")
            bucket.delete(bucket_name)
            bucket.wait_until_not_exists()
            log.info("SUCCESS! Deleted bucket %s", bucket_name)
        except ClientError:
            log.exception("Failed to delete Amazon S3 Bucket", bucket_name=bucket_name)
            return False
        return True

    # Note: ExtraArgs parameter and Callback parameter can be used to implement
    # a progress monitor. Reference for ExtraArgs parameters:
    # https://docs.aws.amazon.com/boto3/latest/reference/
    # customizations/s3.html#boto3.s3.transfer.S3Transfer.ALLOWED_UPLOAD_ARGS
    def download_file(
        self,
        bucket_name: str,
        object_name: str,
        file_name: str,
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
    # Also look into adding more exceptions for file path access
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
        """List objects in the S3 bucket.

        The ``list_files`` method returns a list of object keys
        in the bucket, optionally filtered by a prefix.

        Args:
            prefix: The prefix to filter objects by. Defaults to
                empty string which returns all objects.

        Returns:
            A list of object keys matching the prefix.

        Raises:
            ClientError : If the listing fails due to
                        AWS service errors (logged and caught).

        """
        try:
            response = self._client.list_objects_v2(
                Bucket=self._bucket_name,
                Prefix=prefix)
            contents = response.get("Contents", [])
            return [obj["Key"] for obj in contents]
        except ClientError as exc:
            raise NotImplementedError from exc

    # Note: Batch deletion of multiple files could be added for efficiency
    def delete_file(
        self,
        bucket_name: str,
        object_name: str,
    ) -> bool:
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
            s3.delete_object(bucket_name, object_name)
        except ClientError:
            log.exception(
                "Failed to delete object from Amazon S3 Bucket",
                bucket_name=bucket_name,
                object_name=object_name,
            )
            return False
        return True

#--------------------------------------------HELPERS--------------------------------------------------------------------------
    def _get_session(self) -> boto3.Session:
        """Create a boto3 session using environment variables."""
        return boto3.Session(region_name=os.environ["AWS_REGION"])

    def _validate_file_obj(self, file_obj: BinaryIO) -> None:
        """Validate a file-like object for upload.

        Args:
            file_obj: The file-like object to validate.

        Raises:
            ValueError: If the file object is not readable or not in binary mode.

        """
        try:
            if not file_obj.readable():
                log.error("file_obj must be readable")
                raise ValueError
            if isinstance(file_obj.read(0), str):
                log.error("file_obj must be opened in binary mode, not text mode")
                raise TypeError
        except AttributeError as exc:
            log.exception(
                "file_obj must be a file-like object with a read() method",
            )
            raise ValueError from exc

    def create_multipart_upload(self, key: str) -> bool:
        """Initiate a multipart upload and return the upload ID.

        Must be called before ``upload_part``. The ``UploadId`` in the
        returned response is required for all subsequent ``upload_part``,
        ``complete_multipart_upload``, and ``abort_multipart_upload`` calls.

        Note:
            You must either complete or abort the multipart upload after
            initiating it, otherwise AWS will continue charging for the
            stored parts indefinitely.

        Args:
            key: The S3 object key to upload to.

        Returns:
            True, if multipart upload was successful
            False, if multipart upload was NOT successful

        Raises:
            ValueError  : If ``key`` is empty or starts with a leading slash.
            ClientError : If the request fails due to AWS service errors.

        """
        if not key:
            log.error("Key cannot be empty")
            raise ValueError
        if key.startswith("/"):
            log.error("S3 object key cannot start with a leading slash")
            raise ValueError
        kwargs = {
                "Bucket": self._bucket_name,
                "Key": key,
            }
        try:
            log.info("Initializing Multipart Upload...")
            self._client.create_multipart_upload(**kwargs)
            log.info("SUCCESS! Multipart Upload is completed")
        except ClientError:
            log.exception(
                "Failed Multipart Upload",
                key=key,
                )
            return False
        return True

    def complete_multipart_upload(
        self,
        key: str,
        parts: list[dict[str, Any]],
    ) -> bool:
        """Complete a multipart upload by assembling the uploaded parts.

        Must be called after all ``upload_part`` calls have succeeded.
        Parts are assembled in order of their ``PartNumber``, not the
        order they were uploaded.

        Args:
            key     : The S3 object key supplied to ``create_multipart_upload``.
            parts   : List of dicts collected from each ``upload_part`` response,
                    each containing ``'PartNumber'`` and ``'ETag'``::

                    [
                        {"PartNumber": 1, "ETag": '"abc123..."'},
                        {"PartNumber": 2, "ETag": '"def456..."'},
                    ]

        Returns:
            True, if the uploaded parts was successfuly assembled and uploaded
            False, if uploaded parts was NOT successfuly assembled and uploaded

        Raises:
            ValueError  : If ``key`` is empty or starts with a leading slash.
            ClientError : If the request fails due to AWS service errors,
                        including ``NoSuchUpload`` (404) if the ``upload_id`` is
                        invalid or has already been completed or aborted.

        """
        if not key:
            log.error("Key cannot be empty")
            raise ValueError
        if key.startswith("/"):
            log.error("S3 object key cannot start with a leading slash")
            raise ValueError
        try:
            log.info("Assembling uploaded parts for multipart upload...", key=key)
            self._client.complete_multipart_upload(
                Bucket=self._bucket_name,
                Key=key,
                MultipartUpload={"Parts": parts},
            )
            log.info(
                "SUCESS! All parts are assesmbled and finished uploading")
        except ClientError:
            log.exception(
                "Failed to assemble parts and complete multipart upload",
                key=key,
                parts=parts,
            )
            return False
        return True
