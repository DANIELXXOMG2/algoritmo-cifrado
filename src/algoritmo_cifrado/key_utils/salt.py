"""Salt generation module."""

import os
from typing import Final

DEFAULT_SALT_LENGTH: Final[int] = 16


def generate_salt(length: int = DEFAULT_SALT_LENGTH) -> bytes:
    """
    Generate cryptographically secure random salt.

    Args:
        length: Salt byte length (default: 16)

    Returns:
        bytes: Random salt bytes

    """
    return os.urandom(length)
