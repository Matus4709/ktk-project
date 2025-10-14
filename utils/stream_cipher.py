#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Implementacja szyfru z kluczem bieżącym (Stream Cipher)
"""

import os
import hashlib


def generate_key_stream(seed, length):
    """
    Generuje strumień klucza na podstawie ziarna
    
    Args:
        seed: Ziarno do generowania klucza
        length: Długość strumienia klucza
        
    Returns:
        bytes: Strumień klucza
    """
    if not seed:
        raise ValueError("Ziarno nie może być puste")
    
    # Konwertuj ziarno na bajty jeśli to string
    if isinstance(seed, str):
        seed_bytes = seed.encode('utf-8')
    else:
        seed_bytes = seed
    
    # Użyj SHA-256 do generowania deterministycznego strumienia
    key_stream = bytearray()
    counter = 0
    
    while len(key_stream) < length:
        # Utwórz hash z ziarna + licznik
        data = seed_bytes + counter.to_bytes(4, 'big')
        hash_result = hashlib.sha256(data).digest()
        key_stream.extend(hash_result)
        counter += 1
    
    return bytes(key_stream[:length])


def stream_encrypt(text, key):
    """
    Szyfruje tekst szyfrem z kluczem bieżącym
    
    Args:
        text: Tekst do szyfrowania
        key: Klucz szyfrowania (ziarno)
        
    Returns:
        str: Zaszyfrowany tekst (hex)
    """
    if not text:
        return ""
    
    if not key or not key.strip():
        raise ValueError("Klucz nie może być pusty")
    
    # Konwertuj tekst na bajty
    text_bytes = text.encode('utf-8')
    
    # Wygeneruj strumień klucza
    key_stream = generate_key_stream(key, len(text_bytes))
    
    # Wykonaj XOR między tekstem a strumieniem klucza
    encrypted_bytes = bytearray()
    for i, byte in enumerate(text_bytes):
        encrypted_bytes.append(byte ^ key_stream[i])
    
    # Zwróć jako hex string
    return encrypted_bytes.hex()


def stream_decrypt(encrypted_hex, key):
    """
    Deszyfruje tekst szyfrem z kluczem bieżącym
    
    Args:
        encrypted_hex: Zaszyfrowany tekst (hex)
        key: Klucz deszyfrowania (ziarno)
        
    Returns:
        str: Odszyfrowany tekst
    """
    if not encrypted_hex:
        return ""
    
    if not key or not key.strip():
        raise ValueError("Klucz nie może być pusty")
    
    try:
        # Konwertuj hex string na bajty
        encrypted_bytes = bytes.fromhex(encrypted_hex)
    except ValueError:
        raise ValueError("Nieprawidłowy format hex")
    
    # Wygeneruj strumień klucza
    key_stream = generate_key_stream(key, len(encrypted_bytes))
    
    # Wykonaj XOR między zaszyfrowanymi bajtami a strumieniem klucza
    decrypted_bytes = bytearray()
    for i, byte in enumerate(encrypted_bytes):
        decrypted_bytes.append(byte ^ key_stream[i])
    
    # Konwertuj z powrotem na string
    return decrypted_bytes.decode('utf-8')


def stream_encrypt_file(input_file, output_file, key):
    """
    Szyfruje plik szyfrem z kluczem bieżącym
    
    Args:
        input_file: Ścieżka do pliku wejściowego
        output_file: Ścieżka do pliku wyjściowego
        key: Klucz szyfrowania
        
    Returns:
        bool: True jeśli sukces, False jeśli błąd
    """
    try:
        # Sprawdź czy plik jest tekstowy czy binarny
        try:
            with open(input_file, 'r', encoding='utf-8') as file:
                content = file.read()
            # Jeśli udało się odczytać jako tekst, szyfruj jako tekst
            encrypted_content = stream_encrypt(content, key)
            with open(output_file, 'w', encoding='utf-8') as file:
                file.write(encrypted_content)
        except UnicodeDecodeError:
            # Jeśli nie można odczytać jako tekst, traktuj jako binarny
            return stream_encrypt_binary_file(input_file, output_file, key)
        
        return True
    except Exception as e:
        print(f"Błąd podczas szyfrowania pliku: {e}")
        import traceback
        traceback.print_exc()
        return False


def stream_decrypt_file(input_file, output_file, key):
    """
    Deszyfruje plik szyfrem z kluczem bieżącym
    
    Args:
        input_file: Ścieżka do zaszyfrowanego pliku
        output_file: Ścieżka do pliku wyjściowego
        key: Klucz deszyfrowania
        
    Returns:
        bool: True jeśli sukces, False jeśli błąd
    """
    try:
        # Sprawdź czy plik jest tekstowy czy binarny
        try:
            with open(input_file, 'r', encoding='utf-8') as file:
                content = file.read()
            # Jeśli udało się odczytać jako tekst, deszyfruj jako tekst
            decrypted_content = stream_decrypt(content, key)
            with open(output_file, 'w', encoding='utf-8') as file:
                file.write(decrypted_content)
        except UnicodeDecodeError:
            # Jeśli nie można odczytać jako tekst, traktuj jako binarny
            return stream_decrypt_binary_file(input_file, output_file, key)
        
        return True
    except Exception as e:
        print(f"Błąd podczas deszyfrowania pliku: {e}")
        import traceback
        traceback.print_exc()
        return False


def stream_encrypt_binary_file(input_file, output_file, key):
    """
    Szyfruje plik binarny (PDF, obrazy, itp.) szyfrem z kluczem bieżącym
    
    Args:
        input_file: Ścieżka do pliku wejściowego
        output_file: Ścieżka do pliku wyjściowego
        key: Klucz szyfrowania
        
    Returns:
        bool: True jeśli sukces, False jeśli błąd
    """
    try:
        with open(input_file, 'rb') as file:
            content = file.read()
        
        # Wygeneruj strumień klucza
        key_stream = generate_key_stream(key, len(content))
        
        # Wykonaj XOR między zawartością pliku a strumieniem klucza
        encrypted_bytes = bytearray()
        for i, byte in enumerate(content):
            encrypted_bytes.append(byte ^ key_stream[i])
        
        with open(output_file, 'wb') as file:
            file.write(encrypted_bytes)
        
        return True
    except Exception as e:
        print(f"Błąd podczas szyfrowania pliku binarnego: {e}")
        return False


def stream_decrypt_binary_file(input_file, output_file, key):
    """
    Deszyfruje plik binarny (PDF, obrazy, itp.) szyfrem z kluczem bieżącym
    
    Args:
        input_file: Ścieżka do zaszyfrowanego pliku
        output_file: Ścieżka do pliku wyjściowego
        key: Klucz deszyfrowania
        
    Returns:
        bool: True jeśli sukces, False jeśli błąd
    """
    try:
        with open(input_file, 'rb') as file:
            content = file.read()
        
        # Wygeneruj strumień klucza
        key_stream = generate_key_stream(key, len(content))
        
        # Wykonaj XOR między zaszyfrowaną zawartością a strumieniem klucza
        decrypted_bytes = bytearray()
        for i, byte in enumerate(content):
            decrypted_bytes.append(byte ^ key_stream[i])
        
        with open(output_file, 'wb') as file:
            file.write(decrypted_bytes)
        
        return True
    except Exception as e:
        print(f"Błąd podczas deszyfrowania pliku binarnego: {e}")
        return False


def generate_random_key(length=32):
    """
    Generuje losowy klucz o określonej długości
    
    Args:
        length: Długość klucza w bajtach (domyślnie 32)
        
    Returns:
        str: Losowy klucz w formacie hex
    """
    return os.urandom(length).hex()


def validate_key(key):
    """
    Sprawdza czy klucz jest prawidłowy
    
    Args:
        key: Klucz do sprawdzenia
        
    Returns:
        bool: True jeśli klucz jest prawidłowy
    """
    if not key or not key.strip():
        return False
    
    # Sprawdź czy klucz nie jest zbyt krótki
    if len(key.strip()) < 4:
        return False
    
    return True
