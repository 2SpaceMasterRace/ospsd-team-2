"""Tests for S3Client.complete_multipart_upload method."""

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
        operation_name="CompleteMultipartUpload",
    )


def test_complete_multipart_upload_raises_value_error_on_empty_key(
    mocker: "MockerFixture",
) -> None:
    """Test complete_multipart_upload raises ValueError when key is empty."""
    c = S3Client(bucket_name="my-bucket")
    c._client = mocker.Mock()

    with pytest.raises(ValueError):
        c.complete_multipart_upload(key="", upload_id="u", parts=[])


def test_complete_multipart_upload_raises_value_error_on_leading_slash(
    mocker: "MockerFixture",
) -> None:
    """Test complete_multipart_upload raises ValueError when key starts with '/'."""
    c = S3Client(bucket_name="my-bucket")
    c._client = mocker.Mock()

    with pytest.raises(ValueError):
        c.complete_multipart_upload(key="/bad", upload_id="u", parts=[])


def test_complete_multipart_upload_returns_true_on_success(
    mocker: "MockerFixture",
) -> None:
    """Test complete_multipart_upload returns True on success."""
    fake_client = mocker.Mock()

    c = S3Client(bucket_name="my-bucket")
    c._client = fake_client

    parts = [{"PartNumber": 1, "ETag": "e1"}]
    ok = c.complete_multipart_upload(key="k", upload_id="u", parts=parts)

    assert ok is True
    fake_client.complete_multipart_upload.assert_called_once_with(
        Bucket="my-bucket",
        Key="k",
        UploadId="u",
        MultipartUpload={"Parts": parts},
    )


def test_complete_multipart_upload_returns_false_on_client_error(
    mocker: "MockerFixture",
) -> None:
    """Test complete_multipart_upload returns False on ClientError."""
    fake_client = mocker.Mock()
    fake_client.complete_multipart_upload.side_effect = _client_error()

    c = S3Client(bucket_name="my-bucket")
    c._client = fake_client

    parts = [{"PartNumber": 1, "ETag": "e1"}]
    ok = c.complete_multipart_upload(key="k", upload_id="u", parts=parts)

    assert ok is False
    fake_client.complete_multipart_upload.assert_called_once()