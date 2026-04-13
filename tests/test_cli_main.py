"""Tests for CLI main entry point (argparse interface)."""

import pytest
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch
from io import StringIO

from algoritmo_cifrado.cli.main import main


class TestCLIMain:
    """Test CLI main() entry point via argparse."""

    def test_encrypt_text_via_main(self, capsys):
        """Test encrypt command via main()."""
        with patch(
            "sys.argv",
            ["algoritmo-cifrado", "encrypt", "-i", "Hello", "-p", "testpass"],
        ):
            exit_code = main()
        assert exit_code == 0
        captured = capsys.readouterr()
        # Output should be hex ciphertext
        assert len(captured.out.strip()) > 0

    def test_encrypt_file_via_main(self, tmp_path, capsys):
        """Test encrypt file command via main()."""
        input_file = tmp_path / "input.txt"
        input_file.write_text("Secret content")
        output_file = tmp_path / "output.enc"

        with patch(
            "sys.argv",
            [
                "algoritmo-cifrado",
                "encrypt",
                "-i",
                str(input_file),
                "-o",
                str(output_file),
                "-p",
                "testpass",
            ],
        ):
            exit_code = main()
        assert exit_code == 0
        assert output_file.exists()
        captured = capsys.readouterr()
        assert "Encrypted" in captured.out

    def test_decrypt_file_via_main(self, tmp_path, capsys):
        """Test decrypt command via main() with file roundtrip."""
        from algoritmo_cifrado.cli.commands import encrypt_command

        input_file = tmp_path / "input.txt"
        input_file.write_text("Secret roundtrip content")
        encrypted_file = tmp_path / "encrypted.enc"
        decrypt_output = tmp_path / "decrypted.txt"

        # Encrypt first
        encrypt_command(str(input_file), str(encrypted_file), "mypass")

        # Decrypt via main CLI
        with patch(
            "sys.argv",
            [
                "algoritmo-cifrado",
                "decrypt",
                "-i",
                str(encrypted_file),
                "-o",
                str(decrypt_output),
                "-p",
                "mypass",
            ],
        ):
            exit_code = main()
        assert exit_code == 0
        assert decrypt_output.exists()
        assert decrypt_output.read_text() == "Secret roundtrip content"

    def test_hash_text_via_main(self, capsys):
        """Test hash command via main()."""
        with patch("sys.argv", ["algoritmo-cifrado", "hash", "-i", "Hello, World!"]):
            exit_code = main()
        assert exit_code == 0
        captured = capsys.readouterr()
        # Output should be 64-char hex string (SHA-256)
        hex_str = captured.out.strip()
        assert len(hex_str) == 64
        assert all(c in "0123456789abcdef" for c in hex_str)

    def test_verify_match_via_main(self, capsys):
        """Test verify command with matching fingerprint via main()."""
        from algoritmo_cifrado.hash_utils.sha256 import compute_sha256

        fingerprint = compute_sha256(b"Hello, World!").hex_digest

        with patch(
            "sys.argv",
            ["algoritmo-cifrado", "verify", "-i", "Hello, World!", "-f", fingerprint],
        ):
            exit_code = main()
        assert exit_code == 0
        captured = capsys.readouterr()
        assert "Valid" in captured.out

    def test_verify_mismatch_via_main(self, capsys):
        """Test verify command with mismatched fingerprint via main()."""
        with patch(
            "sys.argv",
            ["algoritmo-cifrado", "verify", "-i", "Hello, World!", "-f", "0" * 64],
        ):
            exit_code = main()
        assert exit_code == 0
        captured = capsys.readouterr()
        assert "Invalid" in captured.out

    def test_error_file_not_found_via_main(self, capsys):
        """Test that missing file error returns exit code 1."""
        with patch(
            "sys.argv",
            [
                "algoritmo-cifrado",
                "decrypt",
                "-i",
                "/nonexistent/file.enc",
                "-p",
                "test",
            ],
        ):
            exit_code = main()
        assert exit_code == 1

    def test_error_integrity_via_main(self, tmp_path, capsys):
        """Test that integrity error (wrong password) returns exit code 1."""
        from algoritmo_cifrado.cli.commands import encrypt_command

        input_file = tmp_path / "input.txt"
        input_file.write_text("Secret data")
        encrypted_file = tmp_path / "encrypted.enc"
        encrypt_command(str(input_file), str(encrypted_file), "correct_pass")

        # Try decrypting with wrong password
        with patch(
            "sys.argv",
            [
                "algoritmo-cifrado",
                "decrypt",
                "-i",
                str(encrypted_file),
                "-p",
                "wrong_pass",
            ],
        ):
            exit_code = main()
        assert exit_code == 1

    def test_error_validation_empty_password_via_main(self, capsys):
        """Test validation error with empty password returns exit code 1."""
        with patch(
            "sys.argv", ["algoritmo-cifrado", "encrypt", "-i", "text", "-p", ""]
        ):
            exit_code = main()
        assert exit_code == 1

    def test_unknown_command_via_main(self):
        """Test that unknown command raises SystemExit."""
        with patch("sys.argv", ["algoritmo-cifrado", "unknown_command"]):
            with pytest.raises(SystemExit):
                main()
