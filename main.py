"""Entry point for the OSPSD Team 2 application."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import structlog

from aws_client_impl import S3Client

if TYPE_CHECKING:
    from cloud_storage_client_api import CloudStorageClient

log: Any = structlog.get_logger()


def main() -> None:
    """Create a cloud storage client and log a greeting."""
    client: CloudStorageClient = S3Client(bucket_name="my-bucket")
    log.info("Created cloud storage client", client=client)
    log.info("Hello from Team 2!")


if __name__ == "__main__":
    main()
