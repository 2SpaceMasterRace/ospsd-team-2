"""Abstract base class for cloud storage clients."""

from abc import ABC, abstractmethod
from typing import Any


class CloudStorageClient(ABC):
    """Abstract base class defining the contract for a cloud storage client."""

    @abstractmethod
    def upload_file(self, local_path: str, remote_path: str) -> str:
        """Upload a file to cloud storage.

        Args:
            local_path: Path to the local file.
            remote_path: Destination path in cloud storage.

        Returns:
            The remote URL or identifier of the uploaded file.

        """

    @abstractmethod
    def download_file(
        self, bucket_name: str, object_name: str, file_name: str,
    ) -> bool:
        """Download a file from cloud storage.

        Args:
            bucket_name: Name of the bucket to download from.
            object_name: Key of the object to download.
            file_name: Local destination path.

        """

    @abstractmethod
    def list_files(self, prefix: str = "") -> list[str]:
        """List files in cloud storage.

        Args:
            prefix: Optional prefix to filter results.

        Returns:
            A list of file paths matching the prefix.

        """

    @abstractmethod
    def delete_file(
        self, bucket_name: str, object_name: str,
    ) -> dict[str, Any]:
        """Delete a file from cloud storage.

        Args:
            bucket_name: Name of the bucket containing the object.
            object_name: Key of the object to delete.

        """
