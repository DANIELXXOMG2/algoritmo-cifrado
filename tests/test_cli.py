"""Tests for CLI commands."""

import pytest
from pathlib import Path

from algoritmo_cifrado.cli.commands import (
    encrypt_command,
    decrypt_command,
    hash_command,
    verify_command,
    CipherResult,
    DecryptResult,
)


class TestCLICommands:
    """Test CLI command functions."""

    def test_cli_encrypt_text(self):
        """Test encrypting text."""
        result = encrypt_command("Hello, World!", None, "password123")

        assert isinstance(result, CipherResult)
        assert len(result.ciphertext) > 0
        assert len(result.salt) == 16
        assert len(result.iv) == 12

    def test_cli_decrypt_text_roundtrip(self):
        """Test encrypt/decrypt roundtrip with text."""
        password = "password123"
        plaintext = "Hello, World!"

        # Encrypt
        encrypt_result = encrypt_command(plaintext, None, password)

        # Write to temp file for decryption
        import tempfile

        with tempfile.NamedTemporaryFile(delete=False, suffix=".enc") as f:
            encrypted_path = f.name
            f.write(encrypt_result.ciphertext)

        try:
            # Decrypt
            decrypt_result = decrypt_command(encrypted_path, None, password)

            assert decrypt_result.verified is True
            assert decrypt_result.plaintext.decode("utf-8") == plaintext
        finally:
            Path(encrypted_path).unlink()

    def test_cli_hash_text(self):
        """Test hashing text."""
        result = hash_command("Hello, World!")

        assert result.algorithm == "SHA-256"
        assert len(result.digest) == 32
        assert len(result.hex_digest) == 64

    def test_cli_verify_match(self):
        """Test verify command with matching fingerprint."""
        text = "Hello, World!"
        fingerprint = hash_command(text)

        result = verify_command(text, fingerprint.hex_digest)

        assert result.is_valid is True

    def test_cli_verify_mismatch(self):
        """Test verify command with mismatched fingerprint."""
        result = verify_command("Hello, World!", "0" * 64)

        assert result.is_valid is False
        assert result.error_message == "Fingerprint mismatch"

    def test_cli_file_encrypt_decrypt_roundtrip(self, tmp_path):
        """Test encrypt/decrypt roundtrip with file."""
        password = "password123"

        # Create input file
        input_file = tmp_path / "input.txt"
        input_file.write_bytes(b"Secret file content")

        encrypted_file = tmp_path / "encrypted.enc"
        decrypt_output = tmp_path / "decrypted.txt"

        # Encrypt file
        encrypt_command(str(input_file), str(encrypted_file), password)

        # Decrypt file
        decrypt_result = decrypt_command(
            str(encrypted_file), str(decrypt_output), password
        )

        assert decrypt_result.verified is True
        assert decrypt_output.read_bytes() == b"Secret file content"
