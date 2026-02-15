import pytest
from cloud_storage_api.client import Client, get_client
from cloud_storage_api.cloud_object import CloudObject

def test_client_is_abstract():
    """Ensures the Client interface cannot be instantiated directly."""
    with pytest.raises(TypeError):
        Client()

def test_cloud_object_is_abstract():
    """Ensures CloudObject cannot be instantiated directly."""
    with pytest.raises(TypeError):
        CloudObject()

def test_get_client_raises_not_implemented():
    """Confirms the factory function exists but is ready for implementation."""
    with pytest.raises(NotImplementedError):
        get_client()