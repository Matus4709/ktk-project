"""
Nowoczesny moduł AES z obsługą trybów ECB, CBC, CTR oraz GCM.
Wykorzystuje bibliotekę cryptography dla poprawności i wydajności.
"""

import os
import hashlib
from typing import Optional, Tuple

from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

from utils.logger import app_logger


MAGIC_BYTE = 0xA1
MODE_IDS = {"ECB": 0, "CBC": 1, "CTR": 2, "GCM": 3}
ID_TO_MODE = {v: k for k, v in MODE_IDS.items()}


def _derive_key(password: str, key_size: int) -> bytes:
    key_bytes = hashlib.sha256(password.encode("utf-8")).digest()
    return key_bytes[: key_size // 8]


def _pack_envelope(mode: str, iv: bytes, tag: bytes, ciphertext: bytes) -> bytes:
    return bytes([MAGIC_BYTE, MODE_IDS[mode], len(iv), len(tag)]) + iv + tag + ciphertext


def _unpack_envelope(data: bytes) -> Tuple[str, bytes, bytes, bytes]:
    if len(data) < 4:
        raise ValueError("Dane są zbyt krótkie aby odczytać nagłówek AES")

    magic, mode_id, iv_len, tag_len = data[:4]
    if magic != MAGIC_BYTE:
        raise ValueError("Nieprawidłowy nagłówek danych AES")

    mode = ID_TO_MODE.get(mode_id)
    if mode is None:
        raise ValueError("Nieznany tryb szyfrowania AES")

    offset = 4
    iv = data[offset : offset + iv_len]
    offset += iv_len
    tag = data[offset : offset + tag_len]
    offset += tag_len
    ciphertext = data[offset:]

    if len(iv) != iv_len or len(tag) != tag_len:
        raise ValueError("Nagłówek AES ma nieprawidłowe długości")

    return mode, iv, tag, ciphertext


class AESCipher:
    """Szyfrowanie/deszyfrowanie AES w trybach ECB, CBC, CTR, GCM."""

    def __init__(self, key_size: int = 128):
        if key_size not in (128, 192, 256):
            raise ValueError("Rozmiar klucza musi być jednym z: 128, 192, 256 bitów")
        self.key_size = key_size

    def _build_cipher(self, key: bytes, mode: str, iv: Optional[bytes], tag: Optional[bytes]) -> Cipher:
        aes_alg = algorithms.AES(key)
        if mode == "ECB":
            cipher_mode = modes.ECB()
        elif mode == "CBC":
            if iv is None or len(iv) != 16:
                raise ValueError("CBC wymaga wektora IV o długości 16 bajtów")
            cipher_mode = modes.CBC(iv)
        elif mode == "CTR":
            if iv is None or len(iv) != 16:
                raise ValueError("CTR wymaga nonce/IV o długości 16 bajtów")
            cipher_mode = modes.CTR(iv)
        elif mode == "GCM":
            if iv is None or len(iv) < 12:
                raise ValueError("GCM wymaga nonce o długości co najmniej 12 bajtów")
            cipher_mode = modes.GCM(iv, tag)
        else:
            raise ValueError(f"Nieobsługiwany tryb AES: {mode}")

        return Cipher(aes_alg, cipher_mode, backend=default_backend())

    def _pad(self, data: bytes) -> bytes:
        padder = padding.PKCS7(128).padder()
        return padder.update(data) + padder.finalize()

    def _unpad(self, data: bytes) -> bytes:
        unpadder = padding.PKCS7(128).unpadder()
        return unpadder.update(data) + unpadder.finalize()

    def _encrypt_bytes(self, data: bytes, password: str, mode: str) -> bytes:
        mode = mode.upper()
        if mode not in MODE_IDS:
            raise ValueError(f"Nieznany tryb AES: {mode}")

        key_bytes = _derive_key(password, self.key_size)
        iv: bytes = b""
        tag: bytes = b""

        if mode == "ECB":
            data = self._pad(data)
            cipher = self._build_cipher(key_bytes, mode, None, None)
            encryptor = cipher.encryptor()
            ciphertext = encryptor.update(data) + encryptor.finalize()
        elif mode == "CBC":
            data = self._pad(data)
            iv = os.urandom(16)
            cipher = self._build_cipher(key_bytes, mode, iv, None)
            encryptor = cipher.encryptor()
            ciphertext = encryptor.update(data) + encryptor.finalize()
        elif mode == "CTR":
            iv = os.urandom(16)
            cipher = self._build_cipher(key_bytes, mode, iv, None)
            encryptor = cipher.encryptor()
            ciphertext = encryptor.update(data) + encryptor.finalize()
        elif mode == "GCM":
            iv = os.urandom(12)
            cipher = self._build_cipher(key_bytes, mode, iv, None)
            encryptor = cipher.encryptor()
            ciphertext = encryptor.update(data) + encryptor.finalize()
            tag = encryptor.tag
        else:
            raise ValueError(f"Nieznany tryb AES: {mode}")

        return _pack_envelope(mode, iv, tag, ciphertext)

    def _decrypt_bytes(self, payload: bytes, password: str) -> bytes:
        mode, iv, tag, ciphertext = _unpack_envelope(payload)
        key_bytes = _derive_key(password, self.key_size)

        cipher = self._build_cipher(key_bytes, mode, iv if iv else None, tag if tag else None)
        decryptor = cipher.decryptor()
        plaintext = decryptor.update(ciphertext) + decryptor.finalize()

        if mode in ("ECB", "CBC"):
            plaintext = self._unpad(plaintext)

        return plaintext

    def encrypt(self, plaintext: str, password: str, mode: str = "CBC") -> str:
        """Zwraca wynik jako hex wraz z nagłówkiem opisującym tryb/IV/tag."""
        app_logger.start_operation(f"AES-{self.key_size} szyfrowanie", "AES", "encrypt")
        payload = self._encrypt_bytes(plaintext.encode("utf-8"), password, mode)
        app_logger.finish_operation(True, f"Szyfrowanie AES-{self.key_size} zakończone w trybie {mode.upper()}")
        return payload.hex()

    def decrypt(self, ciphertext_hex: str, password: str) -> str:
        """Odczytuje nagłówek, dopasowuje tryb i odszyfrowuje tekst."""
        app_logger.start_operation(f"AES-{self.key_size} deszyfrowanie", "AES", "decrypt")
        payload = bytes.fromhex(ciphertext_hex)
        plaintext = self._decrypt_bytes(payload, password)
        app_logger.finish_operation(True, f"Deszyfrowanie AES-{self.key_size} zakończone")
        return plaintext.decode("utf-8")

    def encrypt_file(self, input_file: str, output_file: str, password: str, mode: str = "CBC") -> bool:
        try:
            with open(input_file, "rb") as f_in:
                data = f_in.read()
            payload = self._encrypt_bytes(data, password, mode)
            with open(output_file, "wb") as f_out:
                f_out.write(payload)
            app_logger.info(f"Plik zaszyfrowany AES-{self.key_size} ({mode}) -> {output_file}")
            return True
        except Exception as exc:
            app_logger.error(f"AES file encryption error: {exc}")
            return False
    
    def decrypt_file(self, input_file: str, output_file: str, password: str) -> bool:
        try:
            with open(input_file, "rb") as f_in:
                payload = f_in.read()
            data = self._decrypt_bytes(payload, password)
            with open(output_file, "wb") as f_out:
                f_out.write(data)
            app_logger.info(f"Plik odszyfrowany AES-{self.key_size} -> {output_file}")
            return True
        except Exception as exc:
            app_logger.error(f"AES file decryption error: {exc}")
            return False


# Funkcje pomocnicze dla interfejsu (zachowujemy kompatybilne nazwy)
def aes_encrypt_text(text: str, key: str, key_size: int = 128, mode: str = "CBC") -> str:
    cipher = AESCipher(key_size)
    return cipher.encrypt(text, key, mode)


def aes_decrypt_text(ciphertext: str, key: str, key_size: int = 128) -> str:
    cipher = AESCipher(key_size)
    return cipher.decrypt(ciphertext, key)


def aes_encrypt_file(input_file: str, output_file: str, key: str, key_size: int = 128, mode: str = "CBC") -> bool:
    cipher = AESCipher(key_size)
    return cipher.encrypt_file(input_file, output_file, key, mode)


def aes_decrypt_file(input_file: str, output_file: str, key: str, key_size: int = 128) -> bool:
    cipher = AESCipher(key_size)
    return cipher.decrypt_file(input_file, output_file, key)
