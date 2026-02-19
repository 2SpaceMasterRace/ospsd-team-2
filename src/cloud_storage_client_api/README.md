# cloud-storage-client-api

Abstract base class (ABC) defining the contract for a cloud storage client.

## Role

This package provides the **interface** that all cloud storage implementations must follow. It contains no concrete logic — only abstract method signatures and documentation.

## API

- `CloudStorageClient` — Abstract base class with the following methods:
  - `upload_file(local_path, remote_path) -> str`
  - `download_file(remote_path, local_path) -> None`
  - `list_files(prefix) -> list[str]`
  - `delete_file(remote_path) -> None`

## Dependencies

None — this package is intentionally dependency-free.

## Usage

```python
from cloud_storage_client_api import CloudStorageClient
```

Consumers should type-hint against `CloudStorageClient` and receive a concrete implementation via dependency injection.
