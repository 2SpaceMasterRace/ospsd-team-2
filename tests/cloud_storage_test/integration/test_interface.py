"""Integration tests for CloudStorageClient interface."""

from client import CloudStorageClient


def test_cloud_storage_client_has_expected_methods() -> None:
    """Test that CloudStorageClient interface defines expected abstract methods."""
    required = {"upload_file", "download_file", "list_files", "delete_file"}
    assert required.issubset(set(CloudStorageClient.__abstractmethods__))
