# aws-client-impl

AWS S3 implementation of the cloud storage client interface.

Amazon S3 buckets

An Amazon S3 bucket is a storage location to hold files. S3 files are referred to as objects.

This section describes how to use the AWS SDK for Python to perform common operations on S3 buckets.

You use the AWS SDK for Python (Boto3) to create, configure, and manage AWS services, such as Amazon Elastic Compute Cloud (Amazon EC2) and Amazon Simple Storage Service (Amazon S3). The SDK provides an object-oriented API as well as low-level access to AWS services.

Amazon Simple Storage Service (Amazon S3) is an object storage service that offers scalability, data availability, security, and performance.

This section demonstrates how to use the AWS SDK for Python to access Amazon S3 services.


Using the AWS Common Runtime (CRT)

In addition to the default install of Boto3, you can choose to include the new AWS Common Runtime (CRT). The AWS CRT is a collection of modular packages that serve as a new foundation for AWS SDKs. Each library provides better performance and minimal footprint for the functional area it implements. Using the CRT, SDKs can share the same base code when possible, improving consistency and throughput optimizations across AWS SDKs.

When the AWS CRT is included, Boto3 uses it to incorporate features not otherwise available in the AWS SDK for Python.

You’ll find it used in features like:

    Amazon S3 Multi-Region Access Points

    Amazon S3 Object Integrity

    Amazon EventBridge Global Endpoints

    Login with console credentials


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

# TODOs

https://www.structlog.org/en/stable/logging-best-practices.html
While you should use a proper crash reporter like Sentry in production, structlog has helpers for formatting exceptions for humans and machines.


1. Load S3 bucket locally 


In Amazon S3,
a bucket is a logical container for storing data, while an object is the actual data (file) stored within that container


The Callback parameter

Both upload_file and upload_fileobj accept an optional Callback parameter. The parameter references a class that the Python SDK invokes intermittently during the transfer operation.

Invoking a Python class executes the class’s __call__ method. For each invocation, the class is passed the number of bytes transferred up to that point. This information can be used to implement a progress monitor.

The following Callback setting instructs the Python SDK to create an instance of the ProgressPercentage class. During the upload, the instance’s __call__ method will be invoked intermittently.

s3.upload_file(
    'FILE_NAME', 'amzn-s3-demo-bucket', 'OBJECT_NAME',
    Callback=ProgressPercentage('FILE_NAME')
)

An example implementation of the ProcessPercentage class is shown below.

import os
import sys
import threading

class ProgressPercentage(object):

    def __init__(self, filename):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        # To simplify, assume this is hooked up to a single filename
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            sys.stdout.write(
                "\r%s  %s / %s  (%.2f%%)" % (
                    self._filename, self._seen_so_far, self._size,
                    percentage))
            sys.stdout.flush()

🧠 What does that mean?

In Amazon Web Services S3:

A bucket is like a top-level container.

A key uniquely identifies an object inside that bucket.

S3 does not actually have folders — folders are just part of the key string.

📦 Example

If your S3 console shows:

my-bucket
└── reports
    └── 2025
        └── data.csv

The Key is:

reports/2025/data.csv

        object_name and Key refer to the exact same thing.

        How Python Type Checking Works for Libraries
The Problem
Mypy needs type information for every module you import. Your own code has type hints inline, but third-party libraries might not ship any. When mypy can't find type info, it gives the import-untyped error.

Two ways libraries provide type info:
1. Type Stubs (.pyi files) — External packages
These are separate packages containing only type signatures, no runtime code. For example:

boto3 → install boto3-stubs
requests → install types-requests
They live in packages prefixed with types- or suffixed with -stubs. Mypy finds them automatically once installed.

2. py.typed marker file — Inline types
If a library includes type hints directly in its .py source code (like your cloud_storage_client_api does), it needs to tell mypy "hey, I have types!" by including a py.typed marker file.

What is py.typed?
It's literally an empty file — zero bytes, no content needed. You place it in the package's top-level directory:

cloud_storage_client_api/
├── __init__.py
├── py.typed          ← empty file, just needs to exist
└── client.py
This follows PEP 561. When mypy sees this marker, it knows the package supports type checking and will read the inline type annotations from the .py files.

For your project specifically:
boto3 / botocore: You can't add py.typed to these (they're third-party). Install stubs: uv add --dev boto3-stubs
cloud_storage_client_api: This is your own package. Just create the empty marker file in its package directory.
