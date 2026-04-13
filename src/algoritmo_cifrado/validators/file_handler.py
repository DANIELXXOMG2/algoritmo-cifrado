"""File handling validation and operations module."""

from pathlib import Path
from typing import Any

from ..cipher.exceptions import ValidationError, FileOperationError


def validate_file_path(value: Any) -> Path:
    """
    Validate file path input.

    Args:
        value: Path to validate

    Returns:
        Validated Path object

    Raises:
        ValidationError: If path is invalid
        FileNotFoundError: If file doesn't exist

    """
    if value is None:
        raise ValidationError("File path cannot be None")

    try:
        path = Path(value)
        path = path.resolve()
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")
        if not path.is_file():
            raise ValidationError(f"Path is not a file: {path}")
        return path
    except TypeError:
        raise ValidationError(f"Invalid file path: {value}")


def read_file_bytes(path: Path) -> bytes:
    """
    Read file contents as bytes.

    Args:
        path: Path to file

    Returns:
        File contents as bytes

    Raises:
        IOError: If file cannot be read

    """
    try:
        return path.read_bytes()
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {path}")
    except PermissionError:
        raise IOError(f"Permission denied: {path}")
    except Exception as e:
        raise IOError(f"Failed to read file {path}: {e}")


def write_file_bytes(path: Path, data: bytes) -> None:
    """
    Write bytes to file atomically.

    Args:
        path: Destination path
        data: Bytes to write

    Raises:
        IOError: If file cannot be written

    """
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    except PermissionError:
        raise IOError(f"Permission denied: {path}")
    except Exception as e:
        raise IOError(f"Failed to write file {path}: {e}")
