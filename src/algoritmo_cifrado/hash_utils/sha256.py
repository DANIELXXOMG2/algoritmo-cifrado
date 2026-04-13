"""SHA-256 fingerprinting and verification module."""

from dataclasses import dataclass
from typing import Optional

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.hashes import SHA256


@dataclass
class HashFingerprint:
    """
    Represents a SHA-256 digital fingerprint.

    Attributes:
        algorithm: Hash algorithm used ("SHA-256")
        digest: Raw digest bytes (32 bytes)
        hex_digest: Hexadecimal string representation
    """

    algorithm: str
    digest: bytes

    @property
    def hex_digest(self) -> str:
        """Return hex string representation of digest."""
        return self.digest.hex()


@dataclass
class IntegrityReport:
    """
    Result of an integrity verification operation.

    Attributes:
        is_valid: True if integrity check passed
        expected_fingerprint: Expected SHA-256 fingerprint (hex)
        actual_fingerprint: Actual computed SHA-256 fingerprint (hex)
        error_message: Error description if validation failed
    """

    is_valid: bool
    expected_fingerprint: str
    actual_fingerprint: str
    error_message: Optional[str] = None


def compute_sha256(data: bytes) -> HashFingerprint:
    """
    Compute SHA-256 hash of data.

    Args:
        data: Input bytes to hash

    Returns:
        HashFingerprint object with digest and hex representation

    Raises:
        ValueError: If data is empty

    """
    if len(data) == 0:
        raise ValueError("Data cannot be empty")

    digest = hashes.Hash(SHA256())
    digest.update(data)
    hash_bytes = digest.finalize()
    return HashFingerprint(algorithm="SHA-256", digest=hash_bytes)


def verify_fingerprint(data: bytes, expected_hex: str) -> IntegrityReport:
    """
    Verify data matches expected SHA-256 fingerprint.

    Args:
        data: Input bytes to verify
        expected_hex: Expected SHA-256 fingerprint as hex string

    Returns:
        IntegrityReport with validation result

    """
    if len(data) == 0:
        return IntegrityReport(
            is_valid=False,
            expected_fingerprint=expected_hex,
            actual_fingerprint="",
            error_message="Data cannot be empty",
        )

    actual_fingerprint = compute_sha256(data)
    actual_hex = actual_fingerprint.hex_digest
    is_valid = actual_hex.lower() == expected_hex.lower()

    if not is_valid:
        return IntegrityReport(
            is_valid=False,
            expected_fingerprint=expected_hex,
            actual_fingerprint=actual_hex,
            error_message="Fingerprint mismatch",
        )

    return IntegrityReport(
        is_valid=True, expected_fingerprint=expected_hex, actual_fingerprint=actual_hex
    )
