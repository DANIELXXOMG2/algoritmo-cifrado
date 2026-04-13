"""Tests for SHA-256 hash module."""

import pytest

from algoritmo_cifrado.hash_utils import sha256, HashFingerprint, IntegrityReport


class TestSHA256:
    """Test SHA-256 fingerprinting."""

    def test_compute_sha256_returns_fingerprint(self):
        """Test that compute_sha256 returns HashFingerprint."""
        data = b"Hello, World!"
        result = sha256.compute_sha256(data)

        assert isinstance(result, HashFingerprint)
        assert result.algorithm == "SHA-256"
        assert len(result.digest) == 32  # SHA-256 produces 32 bytes
        assert len(result.hex_digest) == 64  # Hex string is 64 chars

    def test_sha256_deterministic(self):
        """Test that same input produces same hash."""
        data = b"Hello, World!"

        hash1 = sha256.compute_sha256(data)
        hash2 = sha256.compute_sha256(data)

        assert hash1.hex_digest == hash2.hex_digest

    def test_sha256_different_inputs(self):
        """Test that different inputs produce different hashes."""
        hash1 = sha256.compute_sha256(b"Hello")
        hash2 = sha256.compute_sha256(b"World")

        assert hash1.hex_digest != hash2.hex_digest

    def test_verify_fingerprint_match(self):
        """Test fingerprint verification with matching data."""
        data = b"Hello, World!"
        fingerprint = sha256.compute_sha256(data)

        result = sha256.verify_fingerprint(data, fingerprint.hex_digest)

        assert isinstance(result, IntegrityReport)
        assert result.is_valid is True
        assert result.expected_fingerprint == fingerprint.hex_digest
        assert result.actual_fingerprint == fingerprint.hex_digest
        assert result.error_message is None

    def test_verify_fingerprint_mismatch(self):
        """Test fingerprint verification with mismatched data."""
        data = b"Hello, World!"
        fingerprint = sha256.compute_sha256(data)

        result = sha256.verify_fingerprint(b"Tampered!", fingerprint.hex_digest)

        assert result.is_valid is False
        assert result.expected_fingerprint == fingerprint.hex_digest
        assert result.actual_fingerprint != fingerprint.hex_digest
        assert result.error_message == "Fingerprint mismatch"

    def test_sha256_empty_data(self):
        """Test that empty data raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            sha256.compute_sha256(b"")
        assert "empty" in str(exc_info.value).lower()

    def test_verify_fingerprint_empty_data(self):
        """Test verify with empty data returns invalid report."""
        result = sha256.verify_fingerprint(b"", "abc123")

        assert result.is_valid is False
        assert result.error_message == "Data cannot be empty"
