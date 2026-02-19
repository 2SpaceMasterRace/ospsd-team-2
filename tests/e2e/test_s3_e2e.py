import os
import uuid
import pytest

from aws_client_impl.s3_client import S3Client

@pytest.mark.e2e
def test_e2e_upload_list_download_delete(tmp_path):
    bucket = os.getenv("E2E_S3_BUCKET")
    region = os.getenv("AWS_REGION", "us-east-1")
    if not bucket:
        pytest.skip("E2E_S3_BUCKET not set")

    client = S3Client(bucket_name=bucket, region=region)

    # create local file
    local_file = tmp_path / "hello.txt"
    local_file.write_text("hello e2e", encoding="utf-8")

    key = f"e2e/{uuid.uuid4()}.txt"
    client.upload_file(str(local_file), key)

    keys = client.list_files(prefix="e2e/")
    assert key in keys

    downloaded = tmp_path / "downloaded.txt"
    client.download_file(key, str(downloaded))
    assert downloaded.read_text(encoding="utf-8") == "hello e2e"

    client.delete_file(key)
