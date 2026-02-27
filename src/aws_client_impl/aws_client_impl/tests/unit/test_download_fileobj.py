"""Tests for S3Client.download_fileobj method."""

from typing import TYPE_CHECKING

from botocore.exceptions import ClientError

from aws_client_impl.s3_client import S3Client

if TYPE_CHECKING:
    from pathlib import Path

    from pytest_mock import MockerFixture


def _client_error(op: str = "DownloadFileobj") -> ClientError:
    """Create a mock ClientError for testing."""
    return ClientError(
        error_response={"Error": {"Code": "500", "Message": "boom"}},
        operation_name=op,
    )


def test_download_fileobj_returns_true_on_success(
    mocker: MockerFixture, tmp_path: Path,
) -> None:
    """Test that download_fileobj returns True on success."""
    fake_s3 = mocker.Mock()
    mocker.patch("aws_client_impl.s3_client.s3", fake_s3)

    target = tmp_path / "out.bin"

    c = S3Client(bucket_name="ignored")
    ok = c.download_fileobj("my-bucket", "my-key", str(target), "unused")

    assert ok is True
    # ensure it called download_fileobj with a file-like object
    args, _kwargs = fake_s3.download_fileobj.call_args
    assert args[0] == "my-bucket"
    assert args[1] == "my-key"
    assert hasattr(args[2], "write")  # file handle


def test_download_fileobj_returns_false_on_client_error(
    mocker: MockerFixture, tmp_path: Path,
) -> None:
    """Test that download_fileobj returns False on client error."""
    fake_s3 = mocker.Mock()
    fake_s3.download_fileobj.side_effect = _client_error()
    mocker.patch("aws_client_impl.s3_client.s3", fake_s3)

    target = tmp_path / "out.bin"

    c = S3Client(bucket_name="ignored")
    ok = c.download_fileobj("my-bucket", "my-key", str(target), "unused")

    assert ok is False
    fake_s3.download_fileobj.assert_called_once()
