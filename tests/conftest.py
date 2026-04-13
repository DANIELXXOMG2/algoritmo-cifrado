"""Pytest fixtures for Algoritmo de Cifrado tests."""

import os
import pytest
from pathlib import Path

from algoritmo_cifrado.cipher import aes_gcm
from algoritmo_cifrado.key_utils import pbkdf2, salt
from algoritmo_cifrado.validators import file_handler


@pytest.fixture
def sample_password():
    """Sample password for testing."""
    return "test_password_123"


@pytest.fixture
def sample_plaintext():
    """Sample plaintext for testing."""
    return b"Hello, World! This is a test message."


@pytest.fixture
def sample_key(sample_password):
    """Sample derived key for testing."""
    salt_bytes = salt.generate_salt()
    return pbkdf2.derive_key(sample_password, salt_bytes)


@pytest.fixture
def sample_iv():
    """Sample IV for testing."""
    return aes_gcm.generate_iv()


@pytest.fixture
def sample_salt():
    """Sample salt for testing."""
    return salt.generate_salt()


@pytest.fixture
def temp_file(tmp_path):
    """Temporary file path for testing."""
    return tmp_path / "test_file.txt"


@pytest.fixture
def encrypted_file(sample_plaintext, sample_password, tmp_path):
    """Create an encrypted file for testing."""
    from algoritmo_cifrado.cli.commands import encrypt_command

    input_file = tmp_path / "input.txt"
    input_file.write_bytes(sample_plaintext)

    output_file = tmp_path / "encrypted.enc"
    encrypt_command(str(input_file), str(output_file), sample_password)

    return output_file
