"""CLI command functions for encryption, decryption, hashing, and verification."""

import json
import struct
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Dict, Any

from ..cipher import aes_gcm, exceptions
from ..cipher.exceptions import ValidationError, FileOperationError
from ..hash_utils import sha256, HashFingerprint, IntegrityReport
from ..key_utils import pbkdf2, salt
from ..validators import input as input_validators
from ..validators import file_handler as validators

# Binary file format constants
SALT_LENGTH = 16
IV_LENGTH = 12
METADATA_LENGTH_BYTES = 4


@dataclass
class CipherResult:
    """
    Encapsulates the result of an encryption operation.

    Attributes:
        ciphertext: The encrypted data (includes auth tag)
        salt: Random salt used for key derivation
        iv: Initialization vector used for encryption
        key_derivation_params: Metadata about key derivation
    """

    ciphertext: bytes
    salt: bytes
    iv: bytes
    key_derivation_params: Dict[str, Any]


@dataclass
class DecryptResult:
    """
    Encapsulates the result of a decryption operation.

    Attributes:
        plaintext: The decrypted original data
        verified: True if GCM authentication tag verified successfully
    """

    plaintext: bytes
    verified: bool


def encrypt_command(
    input_data: str, output: Optional[str], password: str
) -> CipherResult:
    """
    Encrypt input data with password.

    Args:
        input_data: File path or literal text string
        output: Optional output file path
        password: Encryption password

    Returns:
        CipherResult with ciphertext metadata

    Raises:
        ValidationError: If input is invalid
        FileNotFoundError: If input file not found

    """
    # Validate inputs
    password = input_validators.validate_password(password)

    # Check if input is a file path or literal text
    input_path = Path(input_data)
    if input_path.exists() and input_path.is_file():
        plaintext = validators.read_file_bytes(input_path)
        original_filename = input_path.name
    else:
        # Treat as literal text
        plaintext = input_validators.validate_plaintext(input_data)
        original_filename = "text"

    # Generate salt, IV, and derive key
    salt_bytes = salt.generate_salt()
    iv = aes_gcm.generate_iv()
    key = pbkdf2.derive_key(password, salt_bytes)

    # Encrypt
    ciphertext = aes_gcm.encrypt(plaintext, key, iv)

    # Prepare metadata
    key_derivation_params = {
        "iterations": pbkdf2.DEFAULT_ITERATIONS,
        "key_length": 32,
        "algorithm": "PBKDF2-SHA256",
    }
    metadata = {
        "original_filename": original_filename,
        "original_size": len(plaintext),
        "key_derivation_params": key_derivation_params,
    }
    metadata_json = json.dumps(metadata).encode("utf-8")
    metadata_len = len(metadata_json)

    # Build file format: [salt(16)][iv(12)][meta_len(4)][metadata][ciphertext+tag]
    file_format = (
        salt_bytes + iv + struct.pack(">I", metadata_len) + metadata_json + ciphertext
    )

    # Write to output or return
    if output:
        output_path = Path(output)
        validators.write_file_bytes(output_path, file_format)

    return CipherResult(
        ciphertext=file_format,
        salt=salt_bytes,
        iv=iv,
        key_derivation_params=key_derivation_params,
    )


def decrypt_command(
    input_file: str, output: Optional[str], password: str
) -> DecryptResult:
    """
    Decrypt encrypted file with password.

    Args:
        input_file: Encrypted file path
        output: Optional output file path
        password: Decryption password

    Returns:
        DecryptResult with plaintext

    Raises:
        FileNotFoundError: If input file not found
        InvalidKeyError: If password is wrong
        IntegrityError: If data is tampered

    """
    password = input_validators.validate_password(password)

    # Read encrypted file
    input_path = validators.validate_file_path(input_file)
    encrypted_data = validators.read_file_bytes(input_path)

    # Parse file format: [salt(16)][iv(12)][meta_len(4)][metadata][ciphertext+tag]
    salt_bytes = encrypted_data[:SALT_LENGTH]
    iv = encrypted_data[SALT_LENGTH : SALT_LENGTH + IV_LENGTH]
    metadata_len = struct.unpack(
        ">I",
        encrypted_data[
            SALT_LENGTH + IV_LENGTH : SALT_LENGTH + IV_LENGTH + METADATA_LENGTH_BYTES
        ],
    )[0]
    metadata_json = encrypted_data[
        SALT_LENGTH + IV_LENGTH + METADATA_LENGTH_BYTES : SALT_LENGTH
        + IV_LENGTH
        + METADATA_LENGTH_BYTES
        + metadata_len
    ]
    ciphertext_with_tag = encrypted_data[
        SALT_LENGTH + IV_LENGTH + METADATA_LENGTH_BYTES + metadata_len :
    ]

    # Parse metadata
    metadata = json.loads(metadata_json)

    # Derive key
    key = pbkdf2.derive_key(password, salt_bytes)

    # Decrypt
    try:
        plaintext = aes_gcm.decrypt(ciphertext_with_tag, key, iv)
        verified = True
    except exceptions.IntegrityError:
        verified = False
        plaintext = b""
    except exceptions.InvalidKeyError:
        verified = False
        plaintext = b""

    # Write output if specified
    if output and verified:
        output_path = Path(output)
        validators.write_file_bytes(output_path, plaintext)

    return DecryptResult(plaintext=plaintext, verified=verified)


def hash_command(input_data: str) -> HashFingerprint:
    """
    Compute SHA-256 fingerprint of input.

    Args:
        input_data: File path or text string

    Returns:
        HashFingerprint

    Raises:
        ValidationError: If input is invalid
        FileNotFoundError: If file not found

    """
    # Check if input is a file path or literal text
    input_path = Path(input_data)
    if input_path.exists() and input_path.is_file():
        data = validators.read_file_bytes(input_path)
    else:
        # Treat as literal text
        data = input_validators.validate_plaintext(input_data)

    return sha256.compute_sha256(data)


def verify_command(input_data: str, fingerprint: str) -> IntegrityReport:
    """
    Verify input data matches expected fingerprint.

    Args:
        input_data: File path or text string
        fingerprint: Expected SHA-256 hex fingerprint

    Returns:
        IntegrityReport

    Raises:
        ValidationError: If input is invalid
        FileNotFoundError: If file not found

    """
    # Check if input is a file path or literal text
    input_path = Path(input_data)
    if input_path.exists() and input_path.is_file():
        data = validators.read_file_bytes(input_path)
    else:
        # Treat as literal text
        data = input_validators.validate_plaintext(input_data)

    return sha256.verify_fingerprint(data, fingerprint)
