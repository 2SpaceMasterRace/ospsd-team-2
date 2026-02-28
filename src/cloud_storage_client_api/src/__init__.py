"""Cloud storage client API package."""

from cloud_storage_client_api.src.client import CloudStorageClient as CloudStorageClient
from cloud_storage_client_api.src.client import get_client as get_client

__all__ = ["CloudStorageClient", "get_client"]
