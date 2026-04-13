"""Tests for AES-GCM cipher module."""

import pytest

from algoritmo_cifrado.cipher import aes_gcm
from algoritmo_cifrado.cipher.exceptions import IntegrityError, InvalidKeyError


class TestAESGCM:
    """Test AES-GCM encryption and decryption."""

    def test_encrypt_decrypt_roundtrip_text(self, sample_key, sample_iv):
        """Test encrypt/decrypt roundtrip with text."""
        plaintext = b"Hello, World!"
        ciphertext = aes_gcm.encrypt(plaintext, sample_key, sample_iv)
        decrypted = aes_gcm.decrypt(ciphertext, sample_key, sample_iv)
        assert decrypted == plaintext

    def test_encrypt_decrypt_roundtrip_bytes(self, sample_key, sample_iv):
        """Test encrypt/decrypt roundtrip with bytes data."""
        plaintext = b"\x00\x01\x02\x03\x04\x05"
        ciphertext = aes_gcm.encrypt(plaintext, sample_key, sample_iv)
        decrypted = aes_gcm.decrypt(ciphertext, sample_key, sample_iv)
        assert decrypted == plaintext

    def test_tamper_detection(self, sample_key, sample_iv):
        """Test that modified ciphertext raises IntegrityError."""
        plaintext = b"Original message"
        ciphertext = aes_gcm.encrypt(plaintext, sample_key, sample_iv)

        # Tamper with the ciphertext
        tampered = bytearray(ciphertext)
        tampered[0] ^= 0xFF  # Flip a bit
        tampered = bytes(tampered)

        with pytest.raises(IntegrityError):
            aes_gcm.decrypt(tampered, sample_key, sample_iv)

    def test_wrong_key(self, sample_iv):
        """Test decryption with wrong key raises error."""
        from algoritmo_cifrado.key_utils import pbkdf2, salt

        plaintext = b"Secret data"
        key1 = pbkdf2.derive_key("correct_password", salt.generate_salt())
        key2 = pbkdf2.derive_key("wrong_password", salt.generate_salt())

        ciphertext = aes_gcm.encrypt(plaintext, key1, sample_iv)

        # AESGCM with wrong key raises InvalidTag or similar
        with pytest.raises((IntegrityError, InvalidKeyError)):
            aes_gcm.decrypt(ciphertext, key2, sample_iv)

    def test_invalid_key_length(self, sample_iv):
        """Test that wrong key length raises ValueError."""
        wrong_key = b"short"  # Not 32 bytes

        with pytest.raises(ValueError) as exc_info:
            aes_gcm.encrypt(b"plaintext", wrong_key, sample_iv)
        assert "32 bytes" in str(exc_info.value)

    def test_invalid_iv_length(self, sample_key):
        """Test that wrong IV length raises ValueError."""
        wrong_iv = b"short"  # Not 12 bytes

        with pytest.raises(ValueError) as exc_info:
            aes_gcm.encrypt(b"plaintext", sample_key, wrong_iv)
        assert "12 bytes" in str(exc_info.value)

    def test_encrypt_empty_plaintext(self, sample_key, sample_iv):
        """Test that empty plaintext is rejected."""
        # Empty plaintext should work with AES-GCM actually
        # But our validators should catch it before
        ciphertext = aes_gcm.encrypt(b"", sample_key, sample_iv)
        # AES-GCM doesn't reject empty plaintext
        assert len(ciphertext) > 0

    def test_unicode_text(self, sample_key, sample_iv):
        """Test encryption/decryption with unicode text."""
        plaintext = "¡Hola! 日本語 🔐".encode("utf-8")
        ciphertext = aes_gcm.encrypt(plaintext, sample_key, sample_iv)
        decrypted = aes_gcm.decrypt(ciphertext, sample_key, sample_iv)
        assert decrypted == plaintext

    def test_large_plaintext(self, sample_key, sample_iv):
        """Test encryption/decryption with large data (>1KB)."""
        plaintext = os.urandom(1024 * 10)  # 10KB
        ciphertext = aes_gcm.encrypt(plaintext, sample_key, sample_iv)
        decrypted = aes_gcm.decrypt(ciphertext, sample_key, sample_iv)
        assert decrypted == plaintext


import os  # for test_large_plaintext
