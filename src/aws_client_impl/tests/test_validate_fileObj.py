"""Tests for S3Client._validate_file_obj helper method."""

from typing import TYPE_CHECKING
import io

import pytest

from aws_client_impl.s3_client import S3Client

if TYPE_CHECKING:
    from pytest_mock import MockerFixture


def test_validate_file_obj_raises_value_error_when_not_readable(
    mocker: "MockerFixture",
) -> None:
    """Test _validate_file_obj raises ValueError when file_obj is not readable."""
    c = S3Client(bucket_name="ignored")

    class NotReadable:
        def readable(self) -> bool:
            return False

        def read(self, n: int = -1):
            return b""

    with pytest.raises(ValueError):
        c._validate_file_obj(file_obj=NotReadable())


def test_validate_file_obj_raises_type_error_when_text_mode(
    mocker: "MockerFixture",
) -> None:
    """Test _validate_file_obj raises TypeError when file_obj appears to be text."""
    c = S3Client(bucket_name="ignored")

    class TextLike:
        def readable(self) -> bool:
            return True

        def read(self, n: int = -1):
            # Your code checks: isinstance(file_obj.read(0), str)
            return "" if n == 0 else "hello"

    with pytest.raises(TypeError):
        c._validate_file_obj(file_obj=TextLike())


def test_validate_file_obj_raises_value_error_when_not_file_like(
    mocker: "MockerFixture",
) -> None:
    """Test _validate_file_obj raises ValueError when file_obj lacks required methods."""
    c = S3Client(bucket_name="ignored")

    class NotAFile:
        pass

    with pytest.raises(ValueError):
        c._validate_file_obj(file_obj=NotAFile())  # type: ignore[arg-type]


def test_validate_file_obj_passes_for_binary_file_like(
    mocker: "MockerFixture",
) -> None:
    """Test _validate_file_obj does not raise for a valid binary file-like object."""
    c = S3Client(bucket_name="ignored")

    buf = io.BytesIO(b"abc")  # readable and binary
    # Should not raise:
    c._validate_file_obj(file_obj=buf)