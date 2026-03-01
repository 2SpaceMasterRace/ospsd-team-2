import pytest
from botocore.exceptions import ClientError
from aws_client_impl.src.s3_client import S3Client


def _client_error(op="DownloadFile"):
    return ClientError(
        error_response={"Error": {"Code": "500", "Message": "boom"}},
        operation_name=op,
    )


def test_download_file_returns_true_on_success(mocker):
    fake_s3 = mocker.Mock()
    mocker.patch("aws_client_impl.s3_client.s3", fake_s3)

    c = S3Client(bucket_name="ignored")
    ok = c.download_file("my-bucket", "my-key", "local.txt")

    assert ok is True
    fake_s3.download_file.assert_called_once_with("my-bucket", "my-key", "local.txt")


def test_download_file_returns_false_on_client_error(mocker):
    fake_s3 = mocker.Mock()
    fake_s3.download_file.side_effect = _client_error()
    mocker.patch("aws_client_impl.s3_client.s3", fake_s3)

    c = S3Client(bucket_name="ignored")
    ok = c.download_file("my-bucket", "my-key", "local.txt")

    assert ok is False
    fake_s3.download_file.assert_called_once()