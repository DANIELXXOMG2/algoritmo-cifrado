"""Custom exception hierarchy for Algoritmo de Cifrado."""


class AlgoritmoCifradoError(Exception):
    """Base exception for all Algoritmo de Cifrado errors."""

    pass


class InvalidKeyError(AlgoritmoCifradoError):
    """Raised when decryption fails due to wrong key or password."""

    pass


class IntegrityError(AlgoritmoCifradoError):
    """Raised when ciphertext integrity check fails (tampered data or wrong key)."""

    pass


class ValidationError(AlgoritmoCifradoError):
    """Raised when input validation fails."""

    pass


class FileOperationError(AlgoritmoCifradoError):
    """Raised when file operations fail."""

    pass
