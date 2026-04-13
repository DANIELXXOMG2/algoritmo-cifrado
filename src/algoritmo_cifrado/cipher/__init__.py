"""Cipher module for AES-GCM encryption/decryption."""

from .aes_gcm import encrypt, decrypt, generate_iv
from .exceptions import (
    AlgoritmoCifradoError,
    InvalidKeyError,
    IntegrityError,
    ValidationError,
    FileOperationError,
)

__all__ = [
    "encrypt",
    "decrypt",
    "generate_iv",
    "AlgoritmoCifradoError",
    "InvalidKeyError",
    "IntegrityError",
    "ValidationError",
    "FileOperationError",
]
