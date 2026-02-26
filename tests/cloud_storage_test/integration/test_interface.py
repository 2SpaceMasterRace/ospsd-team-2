from cloud_storage_client_api.client import CloudStorageClient

def test_cloud_storage_client_has_expected_methods():
    required = {"upload_file", "download_file", "list_files", "delete_file"}
    assert required.issubset(set(CloudStorageClient.__abstractmethods__))