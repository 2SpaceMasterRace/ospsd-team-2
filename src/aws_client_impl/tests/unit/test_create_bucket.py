"""Tests for S3Client.create_bucket method."""

from typing import TYPE_CHECKING

from botocore.exceptions import ClientError

from aws_client_impl.src.s3_client import S3Client

if TYPE_CHECKING:
    from pytest_mock import MockerFixture


def _client_error() -> ClientError:
    """Create a mock ClientError for testing."""
    return ClientError(
        error_response={"Error": {"Code": "500", "Message": "boom"}},
        operation_name="CreateBucket",
    )


def test_create_bucket_us_east_1_does_not_send_location_constraint(
    mocker: MockerFixture,
) -> None:
    """Test that us-east-1 region does not send location constraint."""
    fake_client = mocker.Mock()
    mocker.patch("aws_client_impl.s3_client.boto3.client", return_value=fake_client)

    c = S3Client(bucket_name="ignored")
    ok = c.create_bucket(bucket_name="my-bucket", region_name="us-east-1")

    assert ok is True
    fake_client.create_bucket.assert_called_once_with(Bucket="my-bucket")


def test_create_bucket_other_region_sends_location_constraint(
    mocker: MockerFixture,
) -> None:
    """Test that other regions send location constraint."""
    fake_client = mocker.Mock()
    mocker.patch("aws_client_impl.s3_client.boto3.client", return_value=fake_client)

    c = S3Client(bucket_name="ignored")
    ok = c.create_bucket(bucket_name="my-bucket", region_name="us-west-2")

    assert ok is True
    fake_client.create_bucket.assert_called_once_with(
        Bucket="my-bucket",
        CreateBucketConfiguration={"LocationConstraint": "us-west-2"},
    )


def test_create_bucket_returns_false_on_client_error(mocker: MockerFixture) -> None:
    """Test that create_bucket returns False on client error."""
    fake_client = mocker.Mock()
    fake_client.create_bucket.side_effect = _client_error()
    mocker.patch("aws_client_impl.s3_client.boto3.client", return_value=fake_client)

    c = S3Client(bucket_name="ignored")
    ok = c.create_bucket(bucket_name="my-bucket", region_name="us-west-2")

    assert ok is False
    fake_client.create_bucket.assert_called_once()
