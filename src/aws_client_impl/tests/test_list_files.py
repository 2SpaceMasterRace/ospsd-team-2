"""Tests for S3Client.list_files method."""

from typing import TYPE_CHECKING

import pytest
from botocore.exceptions import ClientError

from aws_client_impl.s3_client import S3Client

if TYPE_CHECKING:
    from pytest_mock import MockerFixture


def _client_error() -> ClientError:
    """Create a mock ClientError for testing."""
    return ClientError(
        error_response={"Error": {"Code": "500", "Message": "boom"}},
        operation_name="ListObjectsV2",
    )


def test_list_files_returns_keys_on_success(mocker: "MockerFixture") -> None:
    """Test list_files returns object keys when Contents is present."""
    fake_client = mocker.Mock()
    fake_client.list_objects_v2.return_value = {
        "Contents": [{"Key": "a.txt"}, {"Key": "b.txt"}],
    }

    c = S3Client(bucket_name="my-bucket")
    c._client = fake_client  # use mocked client

    keys = c.list_files(prefix="")

    assert keys == ["a.txt", "b.txt"]
    fake_client.list_objects_v2.assert_called_once_with(
        Bucket="my-bucket",
        Prefix="",
    )


def test_list_files_returns_empty_list_when_no_contents(mocker: "MockerFixture") -> None:
    """Test list_files returns [] when Contents is missing."""
    fake_client = mocker.Mock()
    fake_client.list_objects_v2.return_value = {}

    c = S3Client(bucket_name="my-bucket")
    c._client = fake_client

    keys = c.list_files(prefix="x/")

    assert keys == []
    fake_client.list_objects_v2.assert_called_once_with(
        Bucket="my-bucket",
        Prefix="x/",
    )


def test_list_files_raises_notimplementederror_on_client_error(
    mocker: "MockerFixture",
) -> None:
    """Test list_files raises NotImplementedError on ClientError."""
    fake_client = mocker.Mock()
    fake_client.list_objects_v2.side_effect = _client_error()

    c = S3Client(bucket_name="my-bucket")
    c._client = fake_client

    with pytest.raises(NotImplementedError):
        c.list_files(prefix="")

    fake_client.list_objects_v2.assert_called_once()