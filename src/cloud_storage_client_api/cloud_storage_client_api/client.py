from abc import ABC, abstractmethod

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
        raise NotImplementedError

    @abstractmethod
    def download_file(self, remote_path: str, local_path: str) -> None:
        """Download a file from cloud storage.

        Args:
            remote_path: Path to the file in cloud storage.
            local_path: Local destination path.
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
    def delete_file(self, remote_path: str) -> None:
        """Delete a file from cloud storage.

        Args:
            remote_path: Path to the file in cloud storage.
        """
        raise NotImplementedError

def get_client(*, interactive: bool = False) -> CloudStorageClient:
    """Return an instance of Cloud Storage Client."""
    raise NotImplementedError