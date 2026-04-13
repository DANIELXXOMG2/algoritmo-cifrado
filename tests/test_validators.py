"""Tests for input validators."""

import pytest
from pathlib import Path

from pathlib import Path

import pytest

from algoritmo_cifrado.validators import input as validators
from algoritmo_cifrado.validators import file_handler
from algoritmo_cifrado.cipher.exceptions import ValidationError


class TestInputValidators:
    """Test input validation functions."""

    def test_validate_plaintext_string(self):
        """Test validating string plaintext."""
        result = validators.validate_plaintext("Hello, World!")

        assert isinstance(result, bytes)
        assert result == b"Hello, World!"

    def test_validate_plaintext_bytes(self):
        """Test validating bytes plaintext."""
        result = validators.validate_plaintext(b"Hello, World!")

        assert isinstance(result, bytes)
        assert result == b"Hello, World!"

    def test_validate_plaintext_empty(self):
        """Test that empty plaintext raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            validators.validate_plaintext("")
        assert "empty" in str(exc_info.value).lower()

        with pytest.raises(ValidationError):
            validators.validate_plaintext(b"")

    def test_validate_password_valid(self):
        """Test validating valid passwords."""
        assert validators.validate_password("password123") == "password123"
        assert validators.validate_password(b"password123") == "password123"

    def test_validate_password_empty(self):
        """Test that empty password raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            validators.validate_password("")
        assert "empty" in str(exc_info.value).lower()

        with pytest.raises(ValidationError):
            validators.validate_password(b"")

    def test_validate_password_none(self):
        """Test that None password raises ValidationError."""
        with pytest.raises(ValidationError):
            validators.validate_password(None)


class TestFileHandler:
    """Test file handling functions."""

    def test_validate_file_path_exists(self, temp_file):
        """Test validating existing file path."""
        temp_file.write_bytes(b"test content")

        result = file_handler.validate_file_path(temp_file)

        assert isinstance(result, Path)
        assert result.exists()

    def test_validate_file_path_not_found(self):
        """Test that non-existent path raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            file_handler.validate_file_path("/nonexistent/path/file.txt")

    def test_read_file_bytes(self, temp_file):
        """Test reading file bytes."""
        content = b"Hello, World!"
        temp_file.write_bytes(content)

        result = file_handler.read_file_bytes(temp_file)

        assert result == content

    def test_write_file_bytes(self, tmp_path):
        """Test writing file bytes."""
        content = b"Hello, World!"
        file_path = tmp_path / "output.txt"

        file_handler.write_file_bytes(file_path, content)

        assert file_path.read_bytes() == content

    def test_validate_file_path_none(self):
        """Test that None path raises ValidationError."""
        with pytest.raises(ValidationError):
            file_handler.validate_file_path(None)

    def test_validate_file_path_directory(self, tmp_path):
        """Test that directory path raises ValidationError."""
        with pytest.raises(ValidationError):
            file_handler.validate_file_path(tmp_path)

    def test_validate_plaintext_invalid_type(self):
        """Test that invalid type raises ValidationError."""
        with pytest.raises(ValidationError):
            validators.validate_plaintext(12345)

    def test_validate_plaintext_from_path(self, tmp_path):
        """Test reading plaintext from a file path."""
        test_file = tmp_path / "plaintext.txt"
        test_file.write_bytes(b"File content")
        result = validators.validate_plaintext(test_file)
        assert result == b"File content"

    def test_validate_plaintext_empty_file(self, tmp_path):
        """Test that empty file path raises ValidationError."""
        empty_file = tmp_path / "empty.txt"
        empty_file.write_bytes(b"")
        with pytest.raises(ValidationError):
            validators.validate_plaintext(empty_file)

    def test_validate_plaintext_nonexistent_path(self):
        """Test that nonexistent path raises ValidationError."""
        with pytest.raises(ValidationError):
            validators.validate_plaintext(Path("/nonexistent/file.txt"))

    def test_validate_password_bytes(self):
        """Test validating password from bytes."""
        assert validators.validate_password(b"mypassword") == "mypassword"

    def test_validate_password_invalid_type(self):
        """Test that invalid password type raises ValidationError."""
        with pytest.raises(ValidationError):
            validators.validate_password(12345)

    def test_write_file_bytes_creates_parent_dirs(self, tmp_path):
        """Test that write_file_bytes creates parent directories."""
        nested_path = tmp_path / "a" / "b" / "c" / "output.bin"
        file_handler.write_file_bytes(nested_path, b"nested content")
        assert nested_path.read_bytes() == b"nested content"

    def test_read_file_bytes_not_found(self):
        """Test reading nonexistent file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            file_handler.read_file_bytes(Path("/nonexistent/file.txt"))
