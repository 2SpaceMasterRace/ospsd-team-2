# Contributing to OSPSD Team 2

Thank you for your interest in contributing to OSPSD Team 2! This project is a python wrapper for AWS S3. 

## What This Project Does

This library provides a minimal, clean interface over AWS S3. Think of it as a wrapper: instead of dealing with boto3 directly, credentials, and AWS-specific types, you code against a simple interface. The project is split into two components:

- `cloud_storage_client_api` — the abstract interface (the contract)
- `cloud_storage_client_impl` — the AWS S3 concrete implementation

The two are connected via Dependency Injection: importing the implementation automatically registers it with the interface. You always code against the interface, never the implementation directly.

## Getting Started

```console
$ git clone https://github.com/ospsd-team-2/ospsd-team-2.git
$ cd ospsd-team-2
$ uv sync --group dev
```

## Running Tests

```console
$ uv run pytest
```

## Code Style

This project uses [Ruff](https://docs.astral.sh/ruff/) for linting and formatting:

```console
$ uv run ruff check .
$ uv run ruff format .
```

## Submitting Changes

1. Fork the repository and create a branch from `main`.
2. Make your changes and add tests where appropriate.
3. Ensure all tests pass and there are no linting errors.
4. Open a pull request with a clear description of the change.

## Reporting Issues

Open an issue on GitHub. Please include a minimal reproducible example when reporting bugs.

## CI/CD

We use CircleCI. The pipeline runs ruff, mypy, and all three test suites automatically on every push.