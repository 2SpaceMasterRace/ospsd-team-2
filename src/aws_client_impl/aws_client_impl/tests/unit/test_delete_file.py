import pytest
from botocore.exceptions import ClientError
from aws_client_impl.s3_client import S3Client

def _client_error(op="DeleteObject"):
    return ClientError(
        error_response={"Error": {"Code": "500", "Message": "boom"}},
        operation_name=op,
    )

def test_delete_file_raises_unboundlocalerror_on_client_error(mocker):
    fake_s3 = mocker.Mock()
    fake_s3.delete_object.side_effect = _client_error()
    mocker.patch("aws_client_impl.s3_client.s3", fake_s3)

    c = S3Client(bucket_name="ignored")

    with pytest.raises(UnboundLocalError):
        c.delete_file("my-bucket", "my-key")