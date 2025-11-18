#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Implementacja szyfru z kluczem bieżącym (Stream Cipher)
"""

import os
import hashlib
from utils.logger import app_logger


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
    
    try:
        app_logger.start_operation("Stream Cipher Szyfrowanie Tekstu", "Stream Cipher", "encrypt")
        
        preview_text = text[:50] + "..." if len(text) > 50 else text
        key_preview = key[:20] + "..." if len(key) > 20 else key
        app_logger.add_step("INFO", f"Długość tekstu: {len(text)} znaków",
                          {"przykład_tekstu": preview_text})
        app_logger.add_step("INFO", f"Klucz (ziarno): {key_preview}",
                          explanation="Stream Cipher używa klucza jako 'ziarna' do generowania pseudolosowego strumienia bajtów.\n"
                                    "Każdy bajt tekstu jest szyfrowany przez operację XOR z odpowiadającym bajtem ze strumienia klucza.")
        
        # Konwertuj tekst na bajty
        app_logger.add_step("STEP", "Konwersja tekstu na bajty UTF-8...",
                          explanation="Tekst jest konwertowany na sekwencję bajtów używając kodowania UTF-8.\n"
                                    "Każdy znak może być reprezentowany przez 1-4 bajty w zależności od znaku.")
        text_bytes = text.encode('utf-8')
        preview_bytes = ' '.join(f'{b:02x}' for b in text_bytes[:10]) + ("..." if len(text_bytes) > 10 else "")
        app_logger.add_step("STEP", f"Otrzymano {len(text_bytes)} bajtów",
                          {"przykładowe_bajty": preview_bytes},
                          explanation=f"Tekst '{preview_text}' został przekształcony w {len(text_bytes)} bajtów.\n"
                                    f"Przykładowe bajty (hex): {preview_bytes}")
        
        # Wygeneruj strumień klucza
        app_logger.add_step("STEP", "Generowanie strumienia klucza z ziarna (SHA-256)...",
                          explanation="Strumień klucza jest generowany deterministycznie z ziarna używając funkcji hash SHA-256.\n"
                                    "Ziarno + licznik są hashowane, aby wygenerować pseudolosowy strumień bajtów.\n"
                                    "Ten sam ziarno zawsze generuje ten sam strumień klucza.")
        key_stream = generate_key_stream(key, len(text_bytes))
        preview_key_stream = ' '.join(f'{b:02x}' for b in key_stream[:10]) + ("..." if len(key_stream) > 10 else "")
        app_logger.add_step("STEP", f"Wygenerowano strumień klucza o długości {len(key_stream)} bajtów",
                          {"przykładowy_strumień": preview_key_stream},
                          explanation=f"Ze ziarna '{key_preview}' wygenerowano strumień klucza o długości {len(key_stream)} bajtów.\n"
                                    f"Przykładowe bajty strumienia (hex): {preview_key_stream}\n"
                                    f"Każdy bajt strumienia jest pseudolosowy, ale deterministyczny dla danego ziarna.")
        
        # Wykonaj XOR między tekstem a strumieniem klucza
        app_logger.add_step("STEP", "Wykonywanie operacji XOR na każdym bajcie...",
                          explanation="Operacja XOR (exclusive OR) jest wykonywana między każdym bajtem tekstu a odpowiadającym bajtem strumienia klucza.\n"
                                    "XOR ma właściwość: (A XOR B) XOR B = A, co pozwala na łatwe deszyfrowanie.\n"
                                    "Przykład: bajt 0x41 ('A') XOR 0x23 = 0x62")
        encrypted_bytes = bytearray()
        example_xors = []
        for i, byte in enumerate(text_bytes):
            encrypted_byte = byte ^ key_stream[i]
            encrypted_bytes.append(encrypted_byte)
            if len(example_xors) < 5:
                example_xors.append(f"Bajt {i}: 0x{byte:02x} XOR 0x{key_stream[i]:02x} = 0x{encrypted_byte:02x}")
        
        examples_text = "\n".join(example_xors)
        app_logger.add_step("STEP", f"Zaszyfrowano {len(encrypted_bytes)} bajtów",
                          {"przykłady_XOR": examples_text},
                          explanation=f"Każdy bajt tekstu został zaszyfrowany przez XOR z odpowiadającym bajtem strumienia klucza.\n"
                                    f"Przykłady operacji XOR:\n{examples_text}")
        
        # Zwróć jako hex string
        app_logger.add_step("STEP", "Konwersja zaszyfrowanych bajtów na format hex...",
                          explanation="Zaszyfrowane bajty są konwertowane na reprezentację szesnastkową (hex),\n"
                                    "gdzie każdy bajt jest reprezentowany przez 2 znaki (0-9, a-f).")
        encrypted_hex = encrypted_bytes.hex()
        preview_hex = encrypted_hex[:50] + "..." if len(encrypted_hex) > 50 else encrypted_hex
        app_logger.add_step("INFO", f"Długość zaszyfrowanego tekstu: {len(encrypted_hex)} znaków hex",
                          {"przykład_wyniku_hex": preview_hex})
        
        result_summary = f"Zaszyfrowano {len(text)} znaków do {len(encrypted_hex)} znaków hex"
        app_logger.add_step("SUCCESS", "Szyfrowanie zakończone",
                          explanation=f"Tekst został zaszyfrowany szyfrem strumieniowym.\n"
                                    f"Oryginalny tekst: '{preview_text}'\n"
                                    f"Zaszyfrowany tekst (hex): {preview_hex}\n"
                                    f"Każdy bajt został zaszyfrowany przez XOR z pseudolosowym strumieniem klucza.")
        app_logger.finish_operation(True, result_summary)
        
        return encrypted_hex
    except Exception as e:
        app_logger.add_step("ERROR", f"Błąd podczas szyfrowania: {str(e)}")
        app_logger.finish_operation(False, f"Błąd: {str(e)}")
        raise


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
        app_logger.start_operation("Stream Cipher Deszyfrowanie Tekstu", "Stream Cipher", "decrypt")
        app_logger.add_step("INFO", f"Długość zaszyfrowanego tekstu: {len(encrypted_hex)} znaków hex")
        app_logger.add_step("INFO", f"Klucz (ziarno): {key[:20]}..." if len(key) > 20 else f"Klucz (ziarno): {key}")
        
        # Konwertuj hex string na bajty
        app_logger.add_step("STEP", "Konwersja tekstu hex na bajty...")
        try:
            encrypted_bytes = bytes.fromhex(encrypted_hex)
        except ValueError:
            raise ValueError("Nieprawidłowy format hex")
        app_logger.add_step("STEP", f"Otrzymano {len(encrypted_bytes)} bajtów")
        
        # Wygeneruj strumień klucza
        app_logger.add_step("STEP", "Generowanie strumienia klucza z ziarna (SHA-256)...")
        key_stream = generate_key_stream(key, len(encrypted_bytes))
        app_logger.add_step("STEP", f"Wygenerowano strumień klucza o długości {len(key_stream)} bajtów")
        
        # Wykonaj XOR między zaszyfrowanymi bajtami a strumieniem klucza
        app_logger.add_step("STEP", "Wykonywanie operacji XOR na każdym bajcie...")
        decrypted_bytes = bytearray()
        for i, byte in enumerate(encrypted_bytes):
            decrypted_bytes.append(byte ^ key_stream[i])
        app_logger.add_step("STEP", f"Odszyfrowano {len(decrypted_bytes)} bajtów")
        
        # Konwertuj z powrotem na string
        app_logger.add_step("STEP", "Konwersja bajtów na tekst UTF-8...")
        decrypted_text = decrypted_bytes.decode('utf-8')
        app_logger.add_step("INFO", f"Długość odszyfrowanego tekstu: {len(decrypted_text)} znaków")
        
        result_summary = f"Odszyfrowano {len(encrypted_hex)} znaków hex do {len(decrypted_text)} znaków tekstu"
        app_logger.finish_operation(True, result_summary)
        
        return decrypted_text
    except Exception as e:
        app_logger.add_step("ERROR", f"Błąd podczas deszyfrowania: {str(e)}")
        app_logger.finish_operation(False, f"Błąd: {str(e)}")
        raise


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
