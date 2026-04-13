"""Input validation module."""

from pathlib import Path
from typing import Any, Union

from ..cipher.exceptions import ValidationError


def validate_plaintext(value: Any) -> bytes:
    """
    Validate and normalize plaintext input.

    Args:
        value: Input to validate (str, bytes, or Path)

    Returns:
        Validated bytes

    Raises:
        ValidationError: If invalid type or empty

    """
    if isinstance(value, bytes):
        if len(value) == 0:
            raise ValidationError("Plaintext cannot be empty")
        return value
    elif isinstance(value, str):
        if len(value) == 0:
            raise ValidationError("Plaintext cannot be empty")
        return value.encode("utf-8")
    elif isinstance(value, Path):
        if not value.exists():
            raise ValidationError(f"File not found: {value}")
        content = value.read_bytes()
        if len(content) == 0:
            raise ValidationError("Plaintext cannot be empty")
        return content
    else:
        raise ValidationError(f"Invalid plaintext type: {type(value).__name__}")


def validate_password(value: Any) -> str:
    """
    Validate password input.

    Args:
        value: Password to validate

    Returns:
        Validated password string

    Raises:
        ValidationError: If empty or not string-like

    """
    if value is None:
        raise ValidationError("Password cannot be None")

    if isinstance(value, bytes):
        password = value.decode("utf-8")
    elif isinstance(value, str):
        password = value
    else:
        raise ValidationError(f"Invalid password type: {type(value).__name__}")

    if len(password) == 0:
        raise ValidationError("Password cannot be empty")

    return password
