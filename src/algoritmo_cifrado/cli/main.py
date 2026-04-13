"""Command-line interface entry point for Algoritmo de Cifrado."""

import argparse
import sys

from .commands import (
    encrypt_command,
    decrypt_command,
    hash_command,
    verify_command,
)
from ..cipher.exceptions import (
    AlgoritmoCifradoError,
    ValidationError,
    InvalidKeyError,
    IntegrityError,
    FileOperationError,
)


def main() -> int:
    """
    Main CLI entry point.

    Returns:
        Exit code (0 for success, 1 for error)

    """
    parser = argparse.ArgumentParser(
        prog="algoritmo-cifrado",
        description="AES-GCM encryption with SHA-256 integrity verification",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Encrypt subcommand
    encrypt_parser = subparsers.add_parser("encrypt", help="Encrypt data")
    encrypt_parser.add_argument(
        "--input", "-i", required=True, help="Input file path or text string"
    )
    encrypt_parser.add_argument(
        "--output", "-o", default=None, help="Output file path (default: stdout)"
    )
    encrypt_parser.add_argument(
        "--password", "-p", required=True, help="Encryption password"
    )

    # Decrypt subcommand
    decrypt_parser = subparsers.add_parser("decrypt", help="Decrypt data")
    decrypt_parser.add_argument(
        "--input", "-i", required=True, help="Encrypted file path"
    )
    decrypt_parser.add_argument(
        "--output", "-o", default=None, help="Output file path (default: stdout)"
    )
    decrypt_parser.add_argument(
        "--password", "-p", required=True, help="Decryption password"
    )

    # Hash subcommand
    hash_parser = subparsers.add_parser("hash", help="Compute SHA-256 fingerprint")
    hash_parser.add_argument(
        "--input", "-i", required=True, help="Input file path or text string"
    )

    # Verify subcommand
    verify_parser = subparsers.add_parser("verify", help="Verify fingerprint")
    verify_parser.add_argument(
        "--input", "-i", required=True, help="Input file path or text string"
    )
    verify_parser.add_argument(
        "--fingerprint", "-f", required=True, help="Expected SHA-256 fingerprint (hex)"
    )

    args = parser.parse_args()

    try:
        if args.command == "encrypt":
            result = encrypt_command(args.input, args.output, args.password)
            if args.output is None:
                print(result.ciphertext.hex())
            else:
                print(f"Encrypted to {args.output}")

        elif args.command == "decrypt":
            result = decrypt_command(args.input, args.output, args.password)
            if result.verified:
                if args.output is None:
                    sys.stdout.buffer.write(result.plaintext)
                else:
                    print(f"Decrypted to {args.output}")
            else:
                print(
                    "Error: Integrity check failed — data may be tampered or password is incorrect",
                    file=sys.stderr,
                )
                return 1

        elif args.command == "hash":
            result = hash_command(args.input)
            print(result.hex_digest)

        elif args.command == "verify":
            result = verify_command(args.input, args.fingerprint)
            if result.is_valid:
                print("Valid: Fingerprint matches")
            else:
                print(f"Invalid: {result.error_message}")
                print(f"Expected: {result.expected_fingerprint}")
                print(f"Actual: {result.actual_fingerprint}")

        return 0

    except ValidationError as e:
        print(f"Validation error: {e}", file=sys.stderr)
        return 1
    except FileNotFoundError as e:
        print(f"File not found: {e}", file=sys.stderr)
        return 1
    except InvalidKeyError as e:
        print(f"Decryption error: {e}", file=sys.stderr)
        return 1
    except IntegrityError as e:
        print(f"Integrity error: {e}", file=sys.stderr)
        return 1
    except FileOperationError as e:
        print(f"File operation error: {e}", file=sys.stderr)
        return 1
    except AlgoritmoCifradoError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
