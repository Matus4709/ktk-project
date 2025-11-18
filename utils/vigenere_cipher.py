#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Implementacja szyfru Vigenère
"""

from utils.logger import app_logger

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
    
    try:
        app_logger.start_operation("Vigenere Szyfrowanie Tekstu", "Vigenere", "encrypt")
        
        preview_text = text[:50] + "..." if len(text) > 50 else text
        app_logger.add_step("INFO", f"Długość tekstu: {len(text)} znaków",
                          {"przykład_tekstu": preview_text})
        app_logger.add_step("INFO", f"Klucz oryginalny: {key}",
                          explanation="Szyfr Vigenère używa klucza słownego zamiast stałego przesunięcia.\n"
                                    "Każda litera tekstu jest szyfrowana innym przesunięciem zależnym od pozycji w kluczu.")
        
        # Oczyść klucz - tylko litery
        app_logger.add_step("STEP", "Czyszczenie klucza (tylko litery)...",
                          explanation="Klucz jest czyszczony - usuwane są wszystkie znaki niealfabetyczne,\n"
                                    "a pozostałe litery są konwertowane na wielkie litery dla ujednolicenia.")
        clean_key = ''.join(c.upper() for c in key if c.isalpha())
        if not clean_key:
            raise ValueError("Klucz musi zawierać przynajmniej jedną literę")
        app_logger.add_step("STEP", f"Klucz oczyszczony: {clean_key} (długość: {len(clean_key)})",
                          {"klucz_oryginalny": key, "klucz_oczyszczony": clean_key},
                          explanation=f"Klucz '{key}' został przekształcony w '{clean_key}'.\n"
                                    f"Każda litera klucza określa przesunięcie dla odpowiadającej litery tekstu.\n"
                                    f"Klucz jest powtarzany cyklicznie, jeśli tekst jest dłuższy niż klucz.")
        
        result = ""
        key_index = 0
        letters_count = 0
        example_chars = []
        
        for char in text:
            if char.isalpha():
                letters_count += 1
                original_char = char
                # Określ przesunięcie z klucza
                key_char = clean_key[key_index % len(clean_key)]
                shift = ord(key_char) - ord('A')
                
                # Określ czy to duża czy mała litera
                if char.isupper():
                    # Szyfruj duże litery
                    encrypted_char = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
                    result += encrypted_char
                    if len(example_chars) < 5:
                        example_chars.append(f"'{original_char}' + klucz '{key_char}' (shift={shift}) → '{encrypted_char}'")
                else:
                    # Szyfruj małe litery
                    encrypted_char = chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
                    result += encrypted_char
                    if len(example_chars) < 5:
                        example_chars.append(f"'{original_char}' + klucz '{key_char}' (shift={shift}) → '{encrypted_char}'")
                key_index += 1
            else:
                # Pozostaw znaki niealfabetyczne bez zmian
                result += char
        
        examples_text = "\n".join(example_chars) if example_chars else "Brak liter w tekście"
        app_logger.add_step("STEP", f"Zaszyfrowano {letters_count} liter używając klucza o długości {len(clean_key)}",
                          {"przykłady_przekształceń": examples_text},
                          explanation=f"Algorytm szyfruje każdą literę tekstu używając odpowiadającej litery z klucza:\n"
                                    f"- Klucz '{clean_key}' jest powtarzany cyklicznie\n"
                                    f"- Dla każdej litery tekstu: przesunięcie = pozycja litery z klucza w alfabecie\n"
                                    f"- Przykład: litera 'A' klucza daje przesunięcie 0, 'B' daje 1, 'C' daje 2, itd.\n"
                                    f"- Przykłady przekształceń:\n{examples_text}")
        
        preview_result = result[:50] + "..." if len(result) > 50 else result
        result_summary = f"Zaszyfrowano {len(text)} znaków używając klucza '{clean_key}'"
        app_logger.add_step("SUCCESS", "Szyfrowanie zakończone",
                          {"przykład_wyniku": preview_result},
                          explanation=f"Tekst został zaszyfrowany szyfrem Vigenère.\n"
                                    f"Oryginalny tekst: '{preview_text}'\n"
                                    f"Klucz: '{clean_key}'\n"
                                    f"Zaszyfrowany tekst: '{preview_result}'")
        
        app_logger.finish_operation(True, result_summary)
        
        return result
    except Exception as e:
        app_logger.add_step("ERROR", f"Błąd podczas szyfrowania: {str(e)}")
        app_logger.finish_operation(False, f"Błąd: {str(e)}")
        raise


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
    
    try:
        app_logger.start_operation("Vigenere Deszyfrowanie Tekstu", "Vigenere", "decrypt")
        app_logger.add_step("INFO", f"Długość tekstu: {len(text)} znaków")
        app_logger.add_step("INFO", f"Klucz oryginalny: {key}")
        
        # Oczyść klucz - tylko litery
        app_logger.add_step("STEP", "Czyszczenie klucza (tylko litery)...")
        clean_key = ''.join(c.upper() for c in key if c.isalpha())
        if not clean_key:
            raise ValueError("Klucz musi zawierać przynajmniej jedną literę")
        app_logger.add_step("STEP", f"Klucz oczyszczony: {clean_key} (długość: {len(clean_key)})")
        
        result = ""
        key_index = 0
        letters_count = 0
        
        for char in text:
            if char.isalpha():
                letters_count += 1
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
        
        app_logger.add_step("STEP", f"Odszyfrowano {letters_count} liter używając klucza o długości {len(clean_key)}")
        app_logger.add_step("STEP", f"Pozostawiono {len(text) - letters_count} znaków niealfabetycznych bez zmian")
        result_summary = f"Odszyfrowano {len(text)} znaków używając klucza '{clean_key}'"
        app_logger.finish_operation(True, result_summary)
        
        return result
    except Exception as e:
        app_logger.add_step("ERROR", f"Błąd podczas deszyfrowania: {str(e)}")
        app_logger.finish_operation(False, f"Błąd: {str(e)}")
        raise


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
