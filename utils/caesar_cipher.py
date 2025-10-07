#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Implementacja szyfru Cezara
"""

def caesar_encrypt(text, shift):
    """
    Szyfruje tekst szyfrem Cezara
    
    Args:
        text: Tekst do szyfrowania
        shift: Przesunięcie (1-25)
        
    Returns:
        str: Zaszyfrowany tekst
    """
    if not isinstance(shift, int) or shift < 1 or shift > 25:
        raise ValueError("Przesunięcie musi być liczbą całkowitą od 1 do 25")
    
    result = ""
    for char in text:
        if char.isalpha():
            # Określ czy to duża czy mała litera
            if char.isupper():
                # Szyfruj duże litery
                result += chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            else:
                # Szyfruj małe litery
                result += chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
        else:
            # Pozostaw znaki niealfabetyczne bez zmian
            result += char
    
    return result


def caesar_decrypt(text, shift):
    """
    Deszyfruje tekst szyfrem Cezara
    
    Args:
        text: Zaszyfrowany tekst
        shift: Przesunięcie (1-25)
        
    Returns:
        str: Odszyfrowany tekst
    """
    if not isinstance(shift, int) or shift < 1 or shift > 25:
        raise ValueError("Przesunięcie musi być liczbą całkowitą od 1 do 25")
    
    result = ""
    for char in text:
        if char.isalpha():
            # Określ czy to duża czy mała litera
            if char.isupper():
                # Deszyfruj duże litery
                result += chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
            else:
                # Deszyfruj małe litery
                result += chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
        else:
            # Pozostaw znaki niealfabetyczne bez zmian
            result += char
    
    return result


def caesar_encrypt_file(input_file, output_file, shift):
    """
    Szyfruje plik szyfrem Cezara
    
    Args:
        input_file: Ścieżka do pliku wejściowego
        output_file: Ścieżka do pliku wyjściowego
        shift: Przesunięcie (1-25)
        
    Returns:
        bool: True jeśli sukces, False jeśli błąd
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            content = file.read()
        
        encrypted_content = caesar_encrypt(content, shift)
        
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(encrypted_content)
        
        return True
    except Exception as e:
        print(f"Błąd podczas szyfrowania pliku: {e}")
        return False


def caesar_decrypt_file(input_file, output_file, shift):
    """
    Deszyfruje plik szyfrem Cezara
    
    Args:
        input_file: Ścieżka do zaszyfrowanego pliku
        output_file: Ścieżka do pliku wyjściowego
        shift: Przesunięcie (1-25)
        
    Returns:
        bool: True jeśli sukces, False jeśli błąd
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            content = file.read()
        
        decrypted_content = caesar_decrypt(content, shift)
        
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(decrypted_content)
        
        return True
    except Exception as e:
        print(f"Błąd podczas deszyfrowania pliku: {e}")
        return False
