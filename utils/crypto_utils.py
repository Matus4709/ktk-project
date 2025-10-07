#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Wspólne funkcje szyfrowania i deszyfrowania
"""

import base64
from cryptography.fernet import Fernet


def generate_key_from_password(password: str) -> bytes:
    """Generuje klucz z hasła"""
    return base64.urlsafe_b64encode(password.encode()[:32].ljust(32, b'0'))


def encrypt_text(text: str, password: str = None) -> tuple:
    """
    Szyfruje tekst
    
    Args:
        text: Tekst do szyfrowania
        password: Opcjonalne hasło
        
    Returns:
        tuple: (zaszyfrowany_tekst, klucz)
    """
    if password:
        key = generate_key_from_password(password)
    else:
        key = Fernet.generate_key()
    
    fernet = Fernet(key)
    encrypted_text = fernet.encrypt(text.encode())
    
    return encrypted_text.decode(), key.decode()


def decrypt_text(encrypted_text: str, key: str) -> str:
    """
    Deszyfruje tekst
    
    Args:
        encrypted_text: Zaszyfrowany tekst
        key: Klucz do deszyfrowania
        
    Returns:
        str: Odszyfrowany tekst
    """
    fernet = Fernet(key.encode())
    decrypted_text = fernet.decrypt(encrypted_text.encode())
    return decrypted_text.decode()


def encrypt_file(file_path: str, output_path: str, password: str = None) -> tuple:
    """
    Szyfruje plik
    
    Args:
        file_path: Ścieżka do pliku do szyfrowania
        output_path: Ścieżka do zapisania zaszyfrowanego pliku
        password: Opcjonalne hasło
        
    Returns:
        tuple: (sukces, klucz_lub_błąd)
    """
    try:
        with open(file_path, 'rb') as file:
            file_data = file.read()
        
        if password:
            key = generate_key_from_password(password)
        else:
            key = Fernet.generate_key()
        
        fernet = Fernet(key)
        encrypted_data = fernet.encrypt(file_data)
        
        with open(output_path, 'wb') as file:
            file.write(encrypted_data)
        
        return True, key.decode()
    except Exception as e:
        return False, str(e)


def decrypt_file(file_path: str, output_path: str, key: str) -> tuple:
    """
    Deszyfruje plik
    
    Args:
        file_path: Ścieżka do zaszyfrowanego pliku
        output_path: Ścieżka do zapisania odszyfrowanego pliku
        key: Klucz do deszyfrowania
        
    Returns:
        tuple: (sukces, błąd_lub_None)
    """
    try:
        with open(file_path, 'rb') as file:
            encrypted_data = file.read()
        
        fernet = Fernet(key.encode())
        decrypted_data = fernet.decrypt(encrypted_data)
        
        with open(output_path, 'wb') as file:
            file.write(decrypted_data)
        
        return True, None
    except Exception as e:
        return False, str(e)

