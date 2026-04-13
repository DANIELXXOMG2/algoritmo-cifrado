"""AES-256-GCM encryption and decryption module."""

import os
from typing import Final

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.exceptions import InvalidTag

from .exceptions import IntegrityError, InvalidKeyError

# Constants
KEY_LENGTH: Final[int] = 32  # AES-256
IV_LENGTH: Final[int] = 12  # 96 bits for GCM
AUTH_TAG_LENGTH: Final[int] = 16  # 128 bits


def generate_iv() -> bytes:
    """
    Generate a cryptographically secure random IV/nonce for AES-GCM.

    Returns:
        bytes: 12-byte random nonce

    """
    return os.urandom(IV_LENGTH)


def encrypt(plaintext: bytes, key: bytes, iv: bytes) -> bytes:
    """
    Encrypt plaintext using AES-256-GCM.

    Args:
        plaintext: Data to encrypt
        key: 32-byte encryption key
        iv: 12-byte initialization vector (must be unique per key)

    Returns:
        bytes: Ciphertext with appended GCM authentication tag (16 bytes)

    Raises:
        ValueError: If key or iv length is invalid

    """
    if len(key) != KEY_LENGTH:
        raise ValueError(f"Key must be {KEY_LENGTH} bytes, got {len(key)}")
    if len(iv) != IV_LENGTH:
        raise ValueError(f"IV must be {IV_LENGTH} bytes, got {len(iv)}")

    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(iv, plaintext, None)
    return ciphertext


def decrypt(ciphertext_with_tag: bytes, key: bytes, iv: bytes) -> bytes:
    """
    Decrypt and verify ciphertext using AES-256-GCM.

    Args:
        ciphertext_with_tag: Encrypted data with appended GCM auth tag (16 bytes)
        key: 32-byte decryption key
        iv: 12-byte IV used during encryption

    Returns:
        bytes: Decrypted plaintext

    Raises:
        InvalidKeyError: If key is incorrect
        IntegrityError: If authentication tag verification fails (tampered data)

    """
    if len(key) != KEY_LENGTH:
        raise ValueError(f"Key must be {KEY_LENGTH} bytes, got {len(key)}")
    if len(iv) != IV_LENGTH:
        raise ValueError(f"IV must be {IV_LENGTH} bytes, got {len(iv)}")

    aesgcm = AESGCM(key)
    try:
        plaintext = aesgcm.decrypt(iv, ciphertext_with_tag, None)
        return plaintext
    except InvalidTag:
        # Raised when authentication tag verification fails (tampered data or wrong key)
        raise IntegrityError("Authentication tag verification failed")
    except Exception as e:
        # For other exceptions (wrong key, etc.)
        raise InvalidKeyError("Decryption failed: Invalid key") from e
