from aws_client_impl.s3_client import S3Client

def test_upload_file_calls_boto_and_returns_s3_url(mocker):
    fake_s3 = mocker.Mock()
    mocker.patch("aws_client_impl.s3_client.boto3.client", return_value=fake_s3)

    c = S3Client(bucket_name="my-bucket", region="us-east-1")
    url = c.upload_file("local.txt", "remote.txt")

    fake_s3.upload_file.assert_called_once_with("local.txt", "my-bucket", "remote.txt")
    assert url == "s3://my-bucket/remote.txt"

def test_download_file_calls_boto(mocker):
    fake_s3 = mocker.Mock()
    mocker.patch("aws_client_impl.s3_client.boto3.client", return_value=fake_s3)

    c = S3Client(bucket_name="my-bucket")
    c.download_file("remote.txt", "downloaded.txt")

    fake_s3.download_file.assert_called_once_with("my-bucket", "remote.txt", "downloaded.txt")

def test_list_files_parses_keys(mocker):
    fake_s3 = mocker.Mock()
    mocker.patch("aws_client_impl.s3_client.boto3.client", return_value=fake_s3)

    paginator = mocker.Mock()
    fake_s3.get_paginator.return_value = paginator
    paginator.paginate.return_value = [
        {"Contents": [{"Key": "a.txt"}, {"Key": "b.txt"}]},
        {"Contents": [{"Key": "c.txt"}]},
    ]

    c = S3Client(bucket_name="my-bucket")
    keys = c.list_files(prefix="")

    fake_s3.get_paginator.assert_called_once_with("list_objects_v2")
    assert keys == ["a.txt", "b.txt", "c.txt"]

def test_delete_file_calls_boto(mocker):
    fake_s3 = mocker.Mock()
    mocker.patch("aws_client_impl.s3_client.boto3.client", return_value=fake_s3)

    c = S3Client(bucket_name="my-bucket")
    c.delete_file("remote.txt")

    fake_s3.delete_object.assert_called_once_with(Bucket="my-bucket", Key="remote.txt")
