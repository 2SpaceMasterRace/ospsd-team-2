"""Tests for S3Client.create_multipart_upload method."""

from typing import TYPE_CHECKING

import pytest
from botocore.exceptions import ClientError

from src.s3_client import S3Client

if TYPE_CHECKING:
    from pytest_mock import MockerFixture


def _client_error() -> ClientError:
    """Create a mock ClientError for testing."""
    return ClientError(
        error_response={"Error": {"Code": "500", "Message": "boom"}},
        operation_name="CreateMultipartUpload",
    )


def test_create_multipart_upload_raises_value_error_on_empty_key(
    mocker: "MockerFixture",
) -> None:
    """Test create_multipart_upload raises ValueError when key is empty."""
    c = S3Client(bucket_name="my-bucket")
    c._client = mocker.Mock()

    with pytest.raises(ValueError):
        c.create_multipart_upload(key="")


def test_create_multipart_upload_raises_value_error_on_leading_slash(
    mocker: "MockerFixture",
) -> None:
    """Test create_multipart_upload raises ValueError when key starts with '/'."""
    c = S3Client(bucket_name="my-bucket")
    c._client = mocker.Mock()

    with pytest.raises(ValueError):
        c.create_multipart_upload(key="/bad")


def test_create_multipart_upload_returns_response_on_success(
    mocker: "MockerFixture",
) -> None:
    """Test create_multipart_upload returns boto3 response on success."""
    fake_client = mocker.Mock()
    fake_client.create_multipart_upload.return_value = {"UploadId": "u1"}

    c = S3Client(bucket_name="my-bucket")
    c._client = fake_client

    resp = c.create_multipart_upload(key="k")

    assert resp == {"UploadId": "u1"}
    fake_client.create_multipart_upload.assert_called_once_with(
        Bucket="my-bucket",
        Key="k",
    )


def test_create_multipart_upload_raises_client_error_on_failure(
    mocker: "MockerFixture",
) -> None:
    """Test create_multipart_upload re-raises ClientError on failure."""
    fake_client = mocker.Mock()
    fake_client.create_multipart_upload.side_effect = _client_error()

    c = S3Client(bucket_name="my-bucket")
    c._client = fake_client

    with pytest.raises(ClientError):
        c.create_multipart_upload(key="k")

    fake_client.create_multipart_upload.assert_called_once()