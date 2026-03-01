"""Tests for S3Client.upload_part method."""

from typing import TYPE_CHECKING
import io

import pytest
from botocore.exceptions import ClientError

from aws_client_impl.src.s3_client import S3Client

if TYPE_CHECKING:
    from pytest_mock import MockerFixture


def _client_error() -> ClientError:
    """Create a mock ClientError for testing."""
    return ClientError(
        error_response={"Error": {"Code": "500", "Message": "boom"}},
        operation_name="UploadPart",
    )


def test_upload_part_raises_value_error_on_empty_key(mocker: "MockerFixture") -> None:
    """Test upload_part raises ValueError when key is empty."""
    c = S3Client(bucket_name="my-bucket")
    c._client = mocker.Mock()

    with pytest.raises(ValueError):
        c.upload_part(key="", upload_id="u", part_number=1, body=b"x")


def test_upload_part_raises_value_error_on_leading_slash(mocker: "MockerFixture") -> None:
    """Test upload_part raises ValueError when key starts with '/'."""
    c = S3Client(bucket_name="my-bucket")
    c._client = mocker.Mock()

    with pytest.raises(ValueError):
        c.upload_part(key="/bad", upload_id="u", part_number=1, body=b"x")


def test_upload_part_raises_value_error_on_invalid_part_number(
    mocker: "MockerFixture",
) -> None:
    """Test upload_part raises ValueError when part_number is out of range."""
    c = S3Client(bucket_name="my-bucket")
    c._client = mocker.Mock()

    with pytest.raises(ValueError):
        c.upload_part(key="k", upload_id="u", part_number=0, body=b"x")

    with pytest.raises(ValueError):
        c.upload_part(key="k", upload_id="u", part_number=10001, body=b"x")


def test_upload_part_returns_response_on_success(mocker: "MockerFixture") -> None:
    """Test upload_part returns boto3 response on success."""
    fake_client = mocker.Mock()
    fake_client.upload_part.return_value = {"ETag": "e1"}

    c = S3Client(bucket_name="my-bucket")
    c._client = fake_client

    resp = c.upload_part(key="k", upload_id="u", part_number=1, body=b"abc")

    assert resp == {"ETag": "e1"}
    fake_client.upload_part.assert_called_once_with(
        Bucket="my-bucket",
        Key="k",
        PartNumber=1,
        UploadId="u",
        Body=b"abc",
    )


def test_upload_part_raises_client_error_on_failure(mocker: "MockerFixture") -> None:
    """Test upload_part re-raises ClientError on failure."""
    fake_client = mocker.Mock()
    fake_client.upload_part.side_effect = _client_error()

    c = S3Client(bucket_name="my-bucket")
    c._client = fake_client

    with pytest.raises(ClientError):
        c.upload_part(key="k", upload_id="u", part_number=1, body=io.BytesIO(b"abc"))

    fake_client.upload_part.assert_called_once()