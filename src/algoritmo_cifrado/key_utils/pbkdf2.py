"""PBKDF2-SHA256 key derivation module."""

from typing import Final

from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

# Constants
KEY_LENGTH: Final[int] = 32  # 256 bits for AES-256
DEFAULT_ITERATIONS: Final[int] = 480000  # OWASP 2023 recommendation


def derive_key(
    password: str, salt: bytes, iterations: int = DEFAULT_ITERATIONS
) -> bytes:
    """
    Derive a 32-byte encryption key from a password using PBKDF2-SHA256.

    Args:
        password: User-provided password string
        salt: Random salt bytes (minimum 16 bytes recommended)
        iterations: PBKDF2 iteration count (default: 480,000)

    Returns:
        bytes: 32-byte derived key

    Raises:
        ValueError: If password is empty or salt is too short

    """
    if not password:
        raise ValueError("Password cannot be empty")

    if len(salt) < 16:
        raise ValueError("Salt must be at least 16 bytes")

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_LENGTH,
        salt=salt,
        iterations=iterations,
    )
    key = kdf.derive(password.encode("utf-8"))
    return key
