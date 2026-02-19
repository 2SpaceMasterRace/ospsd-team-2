# aws-client-impl

AWS S3 implementation of the cloud storage client interface.

## Role

This package provides a **concrete implementation** of the `CloudStorageClient` ABC using AWS S3. It fulfills the contract defined in `cloud-storage-client-api`.

## API

- `S3Client(bucket_name, region="us-east-1")` — Concrete class implementing all `CloudStorageClient` methods for AWS S3.

## Dependencies

- `cloud-storage-client-api` — The abstract interface this package implements.

## Usage

```python
from aws_client_impl import S3Client

client = S3Client(bucket_name="my-bucket", region="us-east-1")
```
