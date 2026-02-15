"""Core cloud storage client contract definitions and factory placeholder."""

from abc import ABC, abstractmethod
from collections.abc import Iterator

from cloud_storage_api.cloud_object import CloudObject

class Client(ABC):
    """Abstract base class representing a cloud storage client."""

    @abstractmethod
    def get_object(self, key: str) -> CloudObject:
        """Return metadata for an object by its key."""
        raise NotImplementedError

    @abstractmethod
    def list_objects(self, prefix: str = "", max_results: int = 10) -> Iterator[CloudObject]:
        """Return an iterator of objects under the given prefix."""
        raise NotImplementedError

    @abstractmethod
    def upload(self, key: str, data: bytes) -> bool:
        """Upload an object."""
        raise NotImplementedError
    
    @abstractmethod
    def download(self, key: str) -> bytes:
        """Download an object."""
        raise NotImplementedError

    @abstractmethod
    def delete(self, key: str) -> bool:
        """Delete object from storage."""
        raise NotImplementedError

def get_client(*, interactive: bool = False) -> Client:
    """Return an instance of Cloud Storage Client."""
    raise NotImplementedError
