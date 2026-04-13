"""Tests for key derivation utilities."""

import pytest

from algoritmo_cifrado.key_utils import pbkdf2, salt


class TestPBKDF2:
    """Test PBKDF2 key derivation."""

    def test_derive_key_returns_32_bytes(self, sample_salt):
        """Test that derive_key returns 32 bytes."""
        key = pbkdf2.derive_key("password", sample_salt)

        assert len(key) == 32

    def test_derive_key_deterministic(self, sample_salt):
        """Test that same password+salt produces same key."""
        password = "test_password"

        key1 = pbkdf2.derive_key(password, sample_salt)
        key2 = pbkdf2.derive_key(password, sample_salt)

        assert key1 == key2

    def test_derive_key_different_salt(self):
        """Test that different salts produce different keys."""
        password = "test_password"
        salt1 = salt.generate_salt()
        salt2 = salt.generate_salt()

        key1 = pbkdf2.derive_key(password, salt1)
        key2 = pbkdf2.derive_key(password, salt2)

        assert key1 != key2

    def test_generate_salt_length(self):
        """Test that generate_salt returns correct length."""
        salt_bytes = salt.generate_salt()

        assert len(salt_bytes) == 16  # Default length

        salt_32 = salt.generate_salt(length=32)
        assert len(salt_32) == 32

    def test_generate_salt_randomness(self):
        """Test that generate_salt produces different salts each time."""
        salt1 = salt.generate_salt()
        salt2 = salt.generate_salt()

        assert salt1 != salt2

    def test_derive_key_empty_password(self, sample_salt):
        """Test that empty password raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            pbkdf2.derive_key("", sample_salt)
        assert "empty" in str(exc_info.value).lower()

    def test_derive_key_short_salt(self):
        """Test that short salt raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            pbkdf2.derive_key("password", b"short")
        assert "16 bytes" in str(exc_info.value)
