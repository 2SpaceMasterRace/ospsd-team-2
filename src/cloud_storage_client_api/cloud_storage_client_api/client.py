"""Abstract base class for cloud storage clients."""

from abc import ABC, abstractmethod


class CloudStorageClient(ABC):
    """Abstract base class defining the contract for a cloud storage client."""

    @abstractmethod
    def upload_file(self, key: str, local_path: str) -> bool:
        """Upload a file to cloud storage.

        Args:
            local_path: Path to the local file.
            key: The S3 object key to upload the file to.


        Returns:
            The remote URL or identifier of the uploaded file.

        """
        raise NotImplementedError

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
        self, bucket_name: str, object_name: str,
    ) -> bool:
        """Delete a file from cloud storage.

        Args:
            bucket_name: Name of the bucket containing the object.
            object_name: Key of the object to delete.

        """
        raise NotImplementedError

def get_client(*, interactive: bool = False) -> CloudStorageClient:
    """Return an instance of Cloud Storage Client."""
    raise NotImplementedError
