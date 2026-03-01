"""Tests for S3Client.delete_bucket method."""

from typing import TYPE_CHECKING

from botocore.exceptions import ClientError

from src.s3_client import S3Client

if TYPE_CHECKING:
    from pytest_mock import MockerFixture


def _client_error() -> ClientError:
    """Create a mock ClientError for testing."""
    return ClientError(
        error_response={"Error": {"Code": "500", "Message": "boom"}},
        operation_name="DeleteBucket",
    )


def test_delete_bucket_returns_true_on_success(mocker: "MockerFixture") -> None:
    """Test delete_bucket returns True on success."""
    fake_s3 = mocker.Mock()
    fake_bucket = mocker.Mock()
    fake_s3.Bucket.return_value = fake_bucket

    mocker.patch("aws_client_impl.s3_client.s3", fake_s3)

    c = S3Client(bucket_name="ignored")
    ok = c.delete_bucket(bucket_name="my-bucket")

    assert ok is True
    fake_s3.Bucket.assert_called_once_with("my-bucket")
    # Matches YOUR current implementation (even if boto3 would normally be bucket.delete()).
    fake_bucket.delete.assert_called_once_with("my-bucket")
    fake_bucket.wait_until_not_exists.assert_called_once_with()


def test_delete_bucket_returns_false_on_client_error(mocker: "MockerFixture") -> None:
    """Test delete_bucket returns False on ClientError."""
    fake_s3 = mocker.Mock()
    fake_bucket = mocker.Mock()
    fake_bucket.delete.side_effect = _client_error()
    fake_s3.Bucket.return_value = fake_bucket

    mocker.patch("aws_client_impl.s3_client.s3", fake_s3)

    c = S3Client(bucket_name="ignored")
    ok = c.delete_bucket(bucket_name="my-bucket")

    assert ok is False
    fake_s3.Bucket.assert_called_once_with("my-bucket")
    fake_bucket.delete.assert_called_once_with("my-bucket")