"""Abstract base class for cloud storage clients."""

from abc import ABC, abstractmethod
from typing import BinaryIO


class CloudStorageClient(ABC):
    """Abstract base class defining the contract for a cloud storage client."""

    @abstractmethod
    def upload_file(self, local_path: str, remote_path: str) -> bool:
        """Upload a file to cloud storage.

        Args:
            local_path: Path to the local file.
            remote_path: The S3 object key to upload the file to.


        Returns:
            True if the upload was successful.

        """
        raise NotImplementedError

    @abstractmethod
    def upload_obj(self, file_obj: BinaryIO, remote_path: str) -> bool:
        """Upload a binary file-like object to cloud storage.

        Args:
            file_obj: A file-like object opened in binary mode.
            remote_path: Destination path in cloud storage.

        Returns:
            True if the upload was successful.

        """
        raise NotImplementedError

    @abstractmethod
    def download_file(
        self,
        container: str,
        object_name: str,
        file_name: str,
    ) -> bool:
        """Download a file from cloud storage.

        Args:
            container: Name of the container to download from.
            object_name: Key of the object to download.
            file_name: Local destination path.

        """
        raise NotImplementedError

    @abstractmethod
    def list_files(self, prefix: str = "") -> list[str]:
        """List files in cloud storage.

        Args:
            prefix: Optional prefix to filter results.

        Returns:
            A list of file paths matching the prefix.

        """
        raise NotImplementedError

    @abstractmethod
    def delete_file(
        self,
        container: str,
        object_name: str,
    ) -> bool:
        """Delete a file from cloud storage.

        Args:
            container: Name of the container containing the object.
            object_name: Key of the object to delete.

        """
        raise NotImplementedError


def get_client(*, interactive: bool = False) -> CloudStorageClient:
    """Return an instance of Cloud Storage Client."""
    raise NotImplementedError
