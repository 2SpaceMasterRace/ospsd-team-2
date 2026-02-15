"""Cloud object contract - Core cloud storage object representation"""

from abc import ABC, abstractmethod
from datetime import datetime

class CloudObject(ABC):
    """Abstract base class representing a cloud storage object."""

    @property
    @abstractmethod
    def key(self) -> str:
        """Return the unique identifier (full path) of the object."""
        raise NotImplementedError
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Return the file name."""
        raise NotImplementedError

    @property
    @abstractmethod
    def size_bytes(self) -> int:
        """Return the size of the object in bytes."""
        raise NotImplementedError

    @property
    @abstractmethod
    def content_type(self) -> str:
        """Return the MIME type of the object."""
        raise NotImplementedError

    @property
    @abstractmethod
    def modified_at(self) -> datetime:
        """Return when the object was last modified."""
        raise NotImplementedError

def get_cloud_object(object_id: str, raw_data: dict) -> CloudObject:
    """Return an instance of a CloudObject.

    Args:
        object_id: The unique identifier for the object.
        raw_data: The raw metadata used to construct the object.

    Returns:
        CloudObject: An instance conforming to the CloudObject contract.

    Raises:
        NotImplementedError: If the function is not overridden by an implementation.

    """
    raise NotImplementedError
