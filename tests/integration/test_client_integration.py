"""Integration tests for dependency injection wiring.

This module verifies that importing the aws_client_impl package registers
the S3Client with the cloud_storage_client_api factory, so that
``get_client()`` returns a concrete implementation without callers needing
to know which class they receive.
"""

import pytest

from aws_client_impl.src.s3_client import S3Client
from cloud_storage_client_api.src.client import CloudStorageClient, get_client

pytestmark = pytest.mark.integration


@pytest.mark.circleci
def test_dependency_injection_works() -> None:
    """Importing aws_client_impl registers S3Client with the interface factory."""
    import aws_client_impl  # noqa: F401, PLC0415

    client = get_client()
    assert isinstance(client, CloudStorageClient)
    assert isinstance(client, S3Client)


@pytest.mark.circleci
def test_factory_returns_correct_type() -> None:
    """get_client() consistently returns distinct CloudStorageClient instances."""
    import aws_client_impl  # noqa: F401, PLC0415

    client1 = get_client()
    client2 = get_client()
    assert isinstance(client1, CloudStorageClient)
    assert isinstance(client2, CloudStorageClient)
    assert client1 is not client2