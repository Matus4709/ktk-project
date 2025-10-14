#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Implementacja szyfru Vigenère
"""

def vigenere_encrypt(text, key):
    """
    Szyfruje tekst szyfrem Vigenère
    
    Args:
        text: Tekst do szyfrowania
        key: Klucz szyfrowania (tylko litery)
        
    Returns:
        str: Zaszyfrowany tekst
    """
    if not key or not key.strip():
        raise ValueError("Klucz nie może być pusty")
    
    # Oczyść klucz - tylko litery
    clean_key = ''.join(c.upper() for c in key if c.isalpha())
    if not clean_key:
        raise ValueError("Klucz musi zawierać przynajmniej jedną literę")
    
    result = ""
    key_index = 0
    
    for char in text:
        if char.isalpha():
            # Określ czy to duża czy mała litera
            if char.isupper():
                # Szyfruj duże litery
                shift = ord(clean_key[key_index % len(clean_key)]) - ord('A')
                result += chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            else:
                # Szyfruj małe litery
                shift = ord(clean_key[key_index % len(clean_key)]) - ord('A')
                result += chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
            key_index += 1
        else:
            # Pozostaw znaki niealfabetyczne bez zmian
            result += char
    
    return result


def vigenere_decrypt(text, key):
    """
    Deszyfruje tekst szyfrem Vigenère
    
    Args:
        text: Zaszyfrowany tekst
        key: Klucz deszyfrowania (tylko litery)
        
    Returns:
        str: Odszyfrowany tekst
    """
    if not key or not key.strip():
        raise ValueError("Klucz nie może być pusty")
    
    # Oczyść klucz - tylko litery
    clean_key = ''.join(c.upper() for c in key if c.isalpha())
    if not clean_key:
        raise ValueError("Klucz musi zawierać przynajmniej jedną literę")
    
    result = ""
    key_index = 0
    
    for char in text:
        if char.isalpha():
            # Określ czy to duża czy mała litera
            if char.isupper():
                # Deszyfruj duże litery
                shift = ord(clean_key[key_index % len(clean_key)]) - ord('A')
                result += chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
            else:
                # Deszyfruj małe litery
                shift = ord(clean_key[key_index % len(clean_key)]) - ord('A')
                result += chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
            key_index += 1
        else:
            # Pozostaw znaki niealfabetyczne bez zmian
            result += char
    
    return result


def vigenere_encrypt_file(input_file, output_file, key):
    """
    Szyfruje plik szyfrem Vigenère
    
    Args:
        input_file: Ścieżka do pliku wejściowego
        output_file: Ścieżka do pliku wyjściowego
        key: Klucz szyfrowania
        
    Returns:
        bool: True jeśli sukces, False jeśli błąd
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            content = file.read()
        
        encrypted_content = vigenere_encrypt(content, key)
        
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(encrypted_content)
        
        return True
    except Exception as e:
        print(f"Błąd podczas szyfrowania pliku: {e}")
        return False


def vigenere_decrypt_file(input_file, output_file, key):
    """
    Deszyfruje plik szyfrem Vigenère
    
    Args:
        input_file: Ścieżka do zaszyfrowanego pliku
        output_file: Ścieżka do pliku wyjściowego
        key: Klucz deszyfrowania
        
    Returns:
        bool: True jeśli sukces, False jeśli błąd
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            content = file.read()
        
        decrypted_content = vigenere_decrypt(content, key)
        
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(decrypted_content)
        
        return True
    except Exception as e:
        print(f"Błąd podczas deszyfrowania pliku: {e}")
        return False


def vigenere_encrypt_binary_file(input_file, output_file, key):
    """
    Szyfruje plik binarny (PDF, obrazy, itp.) szyfrem Vigenère na poziomie bajtów
    
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
        
        # Oczyść klucz - tylko litery
        clean_key = ''.join(c.upper() for c in key if c.isalpha())
        if not clean_key:
            raise ValueError("Klucz musi zawierać przynajmniej jedną literę")
        
        # Szyfruj każdy bajt osobno
        encrypted_bytes = bytearray()
        key_index = 0
        
        for byte in content:
            # Zastosuj przesunięcie na podstawie klucza
            shift = ord(clean_key[key_index % len(clean_key)]) - ord('A')
            encrypted_byte = (byte + shift) % 256
            encrypted_bytes.append(encrypted_byte)
            key_index += 1
        
        with open(output_file, 'wb') as file:
            file.write(encrypted_bytes)
        
        return True
    except Exception as e:
        print(f"Błąd podczas szyfrowania pliku binarnego: {e}")
        return False


def vigenere_decrypt_binary_file(input_file, output_file, key):
    """
    Deszyfruje plik binarny (PDF, obrazy, itp.) szyfrem Vigenère na poziomie bajtów
    
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
        
        # Oczyść klucz - tylko litery
        clean_key = ''.join(c.upper() for c in key if c.isalpha())
        if not clean_key:
            raise ValueError("Klucz musi zawierać przynajmniej jedną literę")
        
        # Deszyfruj każdy bajt osobno
        decrypted_bytes = bytearray()
        key_index = 0
        
        for byte in content:
            # Zastosuj odwrotne przesunięcie na podstawie klucza
            shift = ord(clean_key[key_index % len(clean_key)]) - ord('A')
            decrypted_byte = (byte - shift) % 256
            decrypted_bytes.append(decrypted_byte)
            key_index += 1
        
        with open(output_file, 'wb') as file:
            file.write(decrypted_bytes)
        
        return True
    except Exception as e:
        print(f"Błąd podczas deszyfrowania pliku binarnego: {e}")
        return False
