# Contributing

Thank you for your interest in contributing to OSPSD Team 2!

## Getting the Code

```console
$ git clone https://github.com/ospsd-team-2/ospsd-team-2.git
$ cd ospsd-team-2
$ uv sync --group dev
```

## Running the Tests

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
