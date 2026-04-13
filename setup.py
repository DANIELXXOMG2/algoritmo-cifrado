"""Setup configuration for Algoritmo de Cifrado."""

from setuptools import setup, find_packages

setup(
    name="algoritmo-cifrado",
    version="1.0.0",
    description="AES-GCM encryption with SHA-256 integrity verification",
    author="Academic Project",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.10",
    install_requires=[
        "cryptography>=43.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=8.0.0",
            "pytest-cov>=4.0.0",
        ],
        "docs": [
            "python-docx>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "algoritmo-cifrado=algoritmo_cifrado.cli.main:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
