"""
Prosty moduł hashujący SHA-256 z opcjonalną solą.
Uwaga: SHA-256 jest funkcją jednokierunkową – nie da się jej "odszyfrować".
"""

import hashlib
import os
from typing import Optional, Tuple


def generate_salt(length: int = 16) -> bytes:
    """Generuje kryptograficznie losową sól."""
    if length <= 0:
        raise ValueError("Długość soli musi być dodatnia")
    return os.urandom(length)


def _to_bytes(value: str) -> bytes:
    return value.encode("utf-8")


def hash_text(text: str, salt: Optional[bytes] = None) -> Tuple[str, bytes]:
    """
    Hashuje tekst algorytmem SHA-256.

    Returns:
        (hash_hex, salt_bytes)
    """
    salt = salt or generate_salt()
    digest = hashlib.sha256(salt + _to_bytes(text)).hexdigest()
    return digest, salt


def verify_text(text: str, expected_hash_hex: str, salt: bytes) -> bool:
    """Sprawdza, czy hash tekstu z podaną solą zgadza się z oczekiwanym."""
    candidate, _ = hash_text(text, salt)
    return candidate.lower() == expected_hash_hex.lower()


def hash_file(file_path: str, salt: Optional[bytes] = None, chunk_size: int = 65536) -> Tuple[str, bytes]:
    """
    Hashuje plik algorytmem SHA-256 (z solą dodawaną przed pierwszymi bajtami).

    Returns:
        (hash_hex, salt_bytes)
    """
    salt = salt or generate_salt()
    sha = hashlib.sha256()
    sha.update(salt)

    with open(file_path, "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            sha.update(chunk)

    return sha.hexdigest(), salt


def verify_file(file_path: str, expected_hash_hex: str, salt: bytes, chunk_size: int = 65536) -> bool:
    """Sprawdza hash pliku z podaną solą."""
    candidate, _ = hash_file(file_path, salt, chunk_size)
    return candidate.lower() == expected_hash_hex.lower()

