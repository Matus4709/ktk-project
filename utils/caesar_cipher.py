#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Implementacja szyfru Cezara
"""

from utils.logger import app_logger

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
    
    try:
        app_logger.start_operation("Caesar Szyfrowanie Tekstu", "Caesar", "encrypt")
        
        # Pokaż przykładowe dane wejściowe
        preview_text = text[:50] + "..." if len(text) > 50 else text
        app_logger.add_step("INFO", f"Długość tekstu: {len(text)} znaków", 
                          {"przykład_tekstu": preview_text})
        app_logger.add_step("INFO", f"Przesunięcie: {shift}",
                          explanation=f"Szyfr Cezara działa poprzez przesunięcie każdej litery o {shift} pozycji w alfabecie.\n"
                                    f"Na przykład: litera 'A' z przesunięciem {shift} staje się '{chr(ord('A') + shift)}'.\n"
                                    f"Jeśli przesunięcie wykracza poza alfabet (np. 'Z' + {shift}), wracamy do początku (modulo 26).")
        
        result = ""
        letters_count = 0
        example_chars = []
        
        for char in text:
            if char.isalpha():
                letters_count += 1
                original_char = char
                # Określ czy to duża czy mała litera
                if char.isupper():
                    # Szyfruj duże litery
                    encrypted_char = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
                    result += encrypted_char
                    if len(example_chars) < 5:  # Zapisz pierwsze 5 przykładów
                        example_chars.append(f"'{original_char}' → '{encrypted_char}' (pozycja {ord(original_char) - ord('A')} + {shift} = {(ord(original_char) - ord('A') + shift) % 26})")
                else:
                    # Szyfruj małe litery
                    encrypted_char = chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
                    result += encrypted_char
                    if len(example_chars) < 5:
                        example_chars.append(f"'{original_char}' → '{encrypted_char}' (pozycja {ord(original_char) - ord('a')} + {shift} = {(ord(original_char) - ord('a') + shift) % 26})")
            else:
                # Pozostaw znaki niealfabetyczne bez zmian
                result += char
        
        # Dodaj szczegółowe wyjaśnienie z przykładami
        examples_text = "\n".join(example_chars) if example_chars else "Brak liter w tekście"
        app_logger.add_step("STEP", f"Zaszyfrowano {letters_count} liter",
                          {"przykłady_przekształceń": examples_text},
                          explanation=f"Algorytm przeszedł przez każdy znak w tekście:\n"
                                    f"- Dla każdej litery alfabetycznej: obliczono nową pozycję = (pozycja_oryginalna + {shift}) mod 26\n"
                                    f"- Znaki niealfabetyczne (spacje, cyfry, znaki specjalne) pozostają bez zmian\n"
                                    f"- Przykłady przekształceń:\n{examples_text}")
        
        app_logger.add_step("STEP", f"Pozostawiono {len(text) - letters_count} znaków niealfabetycznych bez zmian",
                          explanation="Znaki niealfabetyczne (spacje, interpunkcja, cyfry) nie są szyfrowane,\n"
                                    "aby zachować czytelność struktury tekstu.")
        
        # Pokaż przykładowy wynik
        preview_result = result[:50] + "..." if len(result) > 50 else result
        result_summary = f"Zaszyfrowano {len(text)} znaków z przesunięciem {shift}"
        app_logger.add_step("SUCCESS", "Szyfrowanie zakończone",
                          {"przykład_wyniku": preview_result},
                          explanation=f"Tekst został zaszyfrowany. Każda litera została przesunięta o {shift} pozycji.\n"
                                    f"Oryginalny tekst: '{preview_text}'\n"
                                    f"Zaszyfrowany tekst: '{preview_result}'")
        
        app_logger.finish_operation(True, result_summary)
        
        return result
    except Exception as e:
        app_logger.add_step("ERROR", f"Błąd podczas szyfrowania: {str(e)}")
        app_logger.finish_operation(False, f"Błąd: {str(e)}")
        raise


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
    
    try:
        app_logger.start_operation("Caesar Deszyfrowanie Tekstu", "Caesar", "decrypt")
        
        preview_text = text[:50] + "..." if len(text) > 50 else text
        app_logger.add_step("INFO", f"Długość tekstu: {len(text)} znaków",
                          {"przykład_tekstu": preview_text})
        app_logger.add_step("INFO", f"Przesunięcie: {shift}",
                          explanation=f"Deszyfrowanie działa odwrotnie do szyfrowania - przesuwamy każdą literę o {shift} pozycji WSTECZ.\n"
                                    f"Na przykład: litera '{chr(ord('A') + shift)}' z przesunięciem {shift} wstecz staje się 'A'.\n"
                                    f"Używamy operacji modulo 26, aby obsłużyć przypadki, gdy przesunięcie wykracza poza początek alfabetu.")
        
        result = ""
        letters_count = 0
        example_chars = []
        
        for char in text:
            if char.isalpha():
                letters_count += 1
                original_char = char
                # Określ czy to duża czy mała litera
                if char.isupper():
                    # Deszyfruj duże litery
                    decrypted_char = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
                    result += decrypted_char
                    if len(example_chars) < 5:
                        example_chars.append(f"'{original_char}' → '{decrypted_char}' (pozycja {ord(original_char) - ord('A')} - {shift} = {(ord(original_char) - ord('A') - shift) % 26})")
                else:
                    # Deszyfruj małe litery
                    decrypted_char = chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
                    result += decrypted_char
                    if len(example_chars) < 5:
                        example_chars.append(f"'{original_char}' → '{decrypted_char}' (pozycja {ord(original_char) - ord('a')} - {shift} = {(ord(original_char) - ord('a') - shift) % 26})")
            else:
                # Pozostaw znaki niealfabetyczne bez zmian
                result += char
        
        examples_text = "\n".join(example_chars) if example_chars else "Brak liter w tekście"
        app_logger.add_step("STEP", f"Odszyfrowano {letters_count} liter",
                          {"przykłady_przekształceń": examples_text},
                          explanation=f"Algorytm przeszedł przez każdy znak w zaszyfrowanym tekście:\n"
                                    f"- Dla każdej litery: obliczono oryginalną pozycję = (pozycja_zaszyfrowana - {shift}) mod 26\n"
                                    f"- Znaki niealfabetyczne pozostają bez zmian\n"
                                    f"- Przykłady deszyfrowania:\n{examples_text}")
        
        preview_result = result[:50] + "..." if len(result) > 50 else result
        result_summary = f"Odszyfrowano {len(text)} znaków z przesunięciem {shift}"
        app_logger.add_step("SUCCESS", "Deszyfrowanie zakończone",
                          {"przykład_wyniku": preview_result},
                          explanation=f"Tekst został odszyfrowany. Każda litera została przesunięta o {shift} pozycji wstecz.\n"
                                    f"Zaszyfrowany tekst: '{preview_text}'\n"
                                    f"Odszyfrowany tekst: '{preview_result}'")
        
        app_logger.finish_operation(True, result_summary)
        
        return result
    except Exception as e:
        app_logger.add_step("ERROR", f"Błąd podczas deszyfrowania: {str(e)}")
        app_logger.finish_operation(False, f"Błąd: {str(e)}")
        raise


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


def caesar_encrypt_binary_file(input_file, output_file, shift):
    """
    Szyfruje plik binarny (PDF, obrazy, itp.) szyfrem Cezara na poziomie bajtów
    
    Args:
        input_file: Ścieżka do pliku wejściowego
        output_file: Ścieżka do pliku wyjściowego
        shift: Przesunięcie (1-25)
        
    Returns:
        bool: True jeśli sukces, False jeśli błąd
    """
    try:
        with open(input_file, 'rb') as file:
            content = file.read()
        
        # Szyfruj każdy bajt osobno
        encrypted_bytes = bytearray()
        for byte in content:
            # Zastosuj przesunięcie modulo 256
            encrypted_byte = (byte + shift) % 256
            encrypted_bytes.append(encrypted_byte)
        
        with open(output_file, 'wb') as file:
            file.write(encrypted_bytes)
        
        return True
    except Exception as e:
        print(f"Błąd podczas szyfrowania pliku binarnego: {e}")
        return False


def caesar_decrypt_binary_file(input_file, output_file, shift):
    """
    Deszyfruje plik binarny (PDF, obrazy, itp.) szyfrem Cezara na poziomie bajtów
    
    Args:
        input_file: Ścieżka do zaszyfrowanego pliku
        output_file: Ścieżka do pliku wyjściowego
        shift: Przesunięcie (1-25)
        
    Returns:
        bool: True jeśli sukces, False jeśli błąd
    """
    try:
        with open(input_file, 'rb') as file:
            content = file.read()
        
        # Deszyfruj każdy bajt osobno
        decrypted_bytes = bytearray()
        for byte in content:
            # Zastosuj odwrotne przesunięcie modulo 256
            decrypted_byte = (byte - shift) % 256
            decrypted_bytes.append(decrypted_byte)
        
        with open(output_file, 'wb') as file:
            file.write(decrypted_bytes)
        
        return True
    except Exception as e:
        print(f"Błąd podczas deszyfrowania pliku binarnego: {e}")
        return False
