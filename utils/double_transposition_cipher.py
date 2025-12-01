#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Podwójna transpozycja kolumnowa (Double Columnar Transposition).

Algorytm jest symetryczny: tekst jest dwukrotnie poddawany transpozycji
kolumnowej z różnymi kluczami. Implementacja nie korzysta z zewnętrznych
bibliotek – wszystkie operacje wykonywane są na bajtach w pamięci.
"""

from __future__ import annotations

from typing import List

from utils.logger import app_logger

LENGTH_PREFIX_SIZE = 8  # pozwala obsłużyć pliki do ~16 exabajtów
PAD_BYTE = 0x00


def _normalize_key(key: str, label: str) -> str:
    """Czyści i waliduje klucz."""
    if key is None:
        raise ValueError(f"Klucz {label} jest wymagany.")
    cleaned = "".join(ch for ch in key.strip() if not ch.isspace())
    if len(cleaned) < 2:
        raise ValueError(f"Klucz {label} musi mieć minimum 2 znaki (bez spacji).")
    if len(set(cleaned.upper())) == 1:
        raise ValueError(f"Klucz {label} nie może składać się z identycznych znaków.")
    return cleaned.upper()


def _key_order(key: str) -> List[int]:
    """Zwraca kolejność kolumn dla danego klucza."""
    enumerated = list(enumerate(key))
    enumerated.sort(key=lambda item: (item[1], item[0]))
    return [idx for idx, _ in enumerated]


def _columnar_encrypt(data: bytes, key: str) -> bytes:
    """Jednostopniowa transpozycja kolumnowa."""
    n_cols = len(key)
    if n_cols < 2:
        raise ValueError("Klucz musi mieć minimum 2 znaki.")

    pad_len = (-len(data)) % n_cols
    if pad_len:
        data += bytes([PAD_BYTE]) * pad_len

    n_rows = len(data) // n_cols
    order = _key_order(key)

    matrix = [data[i * n_cols : (i + 1) * n_cols] for i in range(n_rows)]
    columns = []
    for col_idx in order:
        column_bytes = bytearray()
        for row in matrix:
            column_bytes.append(row[col_idx])
        columns.append(bytes(column_bytes))

    return b"".join(columns)


def _columnar_decrypt(data: bytes, key: str) -> bytes:
    """Odwrotność jednego kroku transpozycji kolumnowej."""
    n_cols = len(key)
    if n_cols < 2:
        raise ValueError("Klucz musi mieć minimum 2 znaki.")
    if len(data) % n_cols != 0:
        raise ValueError("Długość danych nie pasuje do klucza transpozycji.")

    n_rows = len(data) // n_cols
    order = _key_order(key)

    columns = {}
    cursor = 0
    for col_idx in order:
        columns[col_idx] = data[cursor : cursor + n_rows]
        cursor += n_rows

    result = bytearray()
    for row in range(n_rows):
        for col in range(n_cols):
            result.append(columns[col][row])
    return bytes(result)


def _double_encrypt(payload: bytes, key_a: str, key_b: str) -> bytes:
    return _columnar_encrypt(_columnar_encrypt(payload, key_a), key_b)


def _double_decrypt(payload: bytes, key_a: str, key_b: str) -> bytes:
    return _columnar_decrypt(_columnar_decrypt(payload, key_b), key_a)


def double_transposition_encrypt_text(plaintext: str, key_a: str, key_b: str) -> str:
    """
    Szyfruje tekst (UTF-8) i zwraca wynik w formacie hex.
    """
    normalized_a = _normalize_key(key_a, "A")
    normalized_b = _normalize_key(key_b, "B")

    app_logger.start_operation(
        "Double Transposition – szyfrowanie tekstu", "DoubleTransposition", "encrypt"
    )
    preview = plaintext[:60] + "..." if len(plaintext) > 60 else plaintext
    app_logger.add_step("INFO", f"Długość tekstu wejściowego: {len(plaintext)} znaków")
    app_logger.add_step("INFO", f"Klucz A: {normalized_a} | Klucz B: {normalized_b}")

    data = plaintext.encode("utf-8")
    payload = len(data).to_bytes(LENGTH_PREFIX_SIZE, "big") + data
    app_logger.add_step(
        "STEP",
        "Dodano prefiks długości i zakodowano dane do UTF-8.",
        {"prefiks_bajtów": LENGTH_PREFIX_SIZE, "podgląd": preview},
    )

    encrypted = _double_encrypt(payload, normalized_a, normalized_b)
    cipher_hex = encrypted.hex()
    preview_hex = cipher_hex[:60] + "..." if len(cipher_hex) > 60 else cipher_hex
    app_logger.add_step(
        "SUCCESS",
        "Podwójna transpozycja zakończona.",
        {"wynik_hex": preview_hex},
    )
    app_logger.finish_operation(True, f"Zaszyfrowano {len(plaintext)} znaków.")
    return cipher_hex


def double_transposition_decrypt_text(cipher_hex: str, key_a: str, key_b: str) -> str:
    """
    Deszyfruje tekst w formacie hex i zwraca ciąg UTF-8.
    """
    normalized_a = _normalize_key(key_a, "A")
    normalized_b = _normalize_key(key_b, "B")

    app_logger.start_operation(
        "Double Transposition – deszyfrowanie tekstu", "DoubleTransposition", "decrypt"
    )
    app_logger.add_step(
        "INFO", f"Długość zaszyfrowanego tekstu: {len(cipher_hex)} znaków hex"
    )

    try:
        data = bytes.fromhex(cipher_hex)
    except ValueError as exc:
        raise ValueError("Nieprawidłowy format hex.") from exc

    decrypted = _double_decrypt(data, normalized_a, normalized_b)
    if len(decrypted) < LENGTH_PREFIX_SIZE:
        raise ValueError("Dane wejściowe są zbyt krótkie.")

    original_len = int.from_bytes(decrypted[:LENGTH_PREFIX_SIZE], "big")
    plaintext_bytes = decrypted[LENGTH_PREFIX_SIZE : LENGTH_PREFIX_SIZE + original_len]
    try:
        plaintext = plaintext_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Nie udało się zdekodować tekstu UTF-8.") from exc

    preview = plaintext[:60] + "..." if len(plaintext) > 60 else plaintext
    app_logger.add_step("SUCCESS", "Deszyfrowanie zakończone.", {"podgląd": preview})
    app_logger.finish_operation(True, f"Odzyskano {len(plaintext)} znaków.")
    return plaintext


def double_transposition_encrypt_file(
    input_path: str, output_path: str, key_a: str, key_b: str
) -> bool:
    """Szyfruje dowolny plik binarny."""
    try:
        normalized_a = _normalize_key(key_a, "A")
        normalized_b = _normalize_key(key_b, "B")

        with open(input_path, "rb") as handle:
            raw = handle.read()

        payload = len(raw).to_bytes(LENGTH_PREFIX_SIZE, "big") + raw
        encrypted = _double_encrypt(payload, normalized_a, normalized_b)

        with open(output_path, "wb") as handle:
            handle.write(encrypted)

        app_logger.info(
            f"DoubleTransposition file encryption OK: {input_path} -> {output_path}"
        )
        return True
    except Exception as exc:  # noqa: BLE001
        app_logger.error(f"DoubleTransposition file encryption failed: {exc}")
        return False


def double_transposition_decrypt_file(
    input_path: str, output_path: str, key_a: str, key_b: str
) -> bool:
    """Deszyfruje plik zaszyfrowany metodą podwójnej transpozycji."""
    try:
        normalized_a = _normalize_key(key_a, "A")
        normalized_b = _normalize_key(key_b, "B")

        with open(input_path, "rb") as handle:
            data = handle.read()

        decrypted = _double_decrypt(data, normalized_a, normalized_b)
        if len(decrypted) < LENGTH_PREFIX_SIZE:
            raise ValueError("Plik nie zawiera prefiksu długości.")

        original_len = int.from_bytes(decrypted[:LENGTH_PREFIX_SIZE], "big")
        payload = decrypted[LENGTH_PREFIX_SIZE : LENGTH_PREFIX_SIZE + original_len]

        with open(output_path, "wb") as handle:
            handle.write(payload)

        app_logger.info(
            f"DoubleTransposition file decryption OK: {input_path} -> {output_path}"
        )
        return True
    except Exception as exc:  # noqa: BLE001
        app_logger.error(f"DoubleTransposition file decryption failed: {exc}")
        return False


