# Changelog

Wszystkie znaczące zmiany w projekcie będą dokumentowane w tym pliku.

Format jest oparty na [Keep a Changelog](https://keepachangelog.com/pl/1.0.0/),
a projekt używa [Semantic Versioning](https://semver.org/lang/pl/).

## [2.0.0] - 2025-10-22

### Dodane
- **Nowa metoda szyfrowania AES** - Advanced Encryption Standard
  - Implementacja AES od podstaw bez korzystania z zewnętrznych bibliotek
  - Obsługa wszystkich rozmiarów klucza: 128, 192, 256 bitów
  - Pełna implementacja wszystkich komponentów AES:
    - S-box i odwrotny S-box
    - ShiftRows i odwrotny ShiftRows
    - MixColumns i odwrotny MixColumns
    - AddRoundKey
    - Rozszerzanie klucza (Key Expansion)
    - Mnożenie w polu Galois GF(2^8)
  - Padding PKCS#7 dla danych
  - Obsługa szyfrowania tekstu i plików binarnych

- **Nowe okna interfejsu użytkownika dla AES**:
  - `views/encrypt_text_aes.py` - Szyfrowanie tekstu AES
  - `views/decrypt_text_aes.py` - Deszyfrowanie tekstu AES
  - `views/encrypt_file_aes.py` - Szyfrowanie plików AES
  - `views/decrypt_file_aes.py` - Deszyfrowanie plików AES

- **Integracja AES z główną aplikacją**:
  - Przycisk AES w menu wyboru szyfru
  - Obsługa wszystkich operacji: tekst/plik, szyfrowanie/deszyfrowanie
  - Wybór rozmiaru klucza (128/192/256 bitów)
  - Nowoczesny interfejs z gradientami i animacjami

- **Ulepszone funkcjonalności**:
  - Obsługa plików binarnych (obrazy, dokumenty, archiwa)
  - Walidacja danych wejściowych
  - Szczegółowe logowanie operacji
  - Obsługa błędów z informatywnymi komunikatami
  - Paski postępu dla operacji na plikach

### Zmienione
- **Zaktualizowano README.md**:
  - Dodano informacje o metodzie AES
  - Zaktualizowano strukturę projektu
  - Rozszerzono instrukcje użytkowania
  - Dodano opis wszystkich metod szyfrowania

- **Poprawiono system logowania**:
  - Usunięto emoji z logów (problemy z kodowaniem Unicode)
  - Uproszczono komunikaty logowania
  - Poprawiono obsługę błędów w loggerze

### Naprawione
- **Krytyczne błędy w deszyfrowaniu plików AES**:
  - Poprawiono logikę usuwania paddingu PKCS#7
  - Naprawiono deszyfrowanie plików binarnych
  - Dodano walidację rozmiaru plików
  - Poprawiono obsługę błędów podczas deszyfrowania

- **Błędy w AppLogger**:
  - Poprawiono inicjalizację loggera w plikach AES
  - Usunięto nieprawidłowe argumenty w konstruktorze

### Usunięte
- **Niepotrzebne pliki**:
  - `requirement-deszyfr.txt` - niepotrzebny plik
  - `requirement-szyfrowane.txt` - niepotrzebny plik
  - Pliki testowe po weryfikacji

## [1.0.0] - 2025-10-22

### Dodane
- **Podstawowa aplikacja szyfrowania/deszyfrowania**
- **Trzy metody szyfrowania**:
  - Szyfr Cezara - klasyczny szyfr przesuwający
  - Szyfr Vigenère - szyfr polialfabetyczny z kluczem
  - Szyfr z kluczem bieżącym - Stream cipher z deterministycznym strumieniem

- **Interfejs użytkownika**:
  - Główne okno aplikacji
  - Okna wyboru typu operacji (szyfrowanie/deszyfrowanie)
  - Okna wyboru typu danych (tekst/plik)
  - Okna wyboru metody szyfrowania
  - Dedykowane okna dla każdej metody szyfrowania

- **Funkcjonalności**:
  - Szyfrowanie i deszyfrowanie tekstu
  - Szyfrowanie i deszyfrowanie plików
  - Obsługa plików tekstowych i binarnych
  - Nowoczesny interfejs GUI z PyQt5
  - System logowania operacji
  - Obsługa błędów i walidacja danych

- **Struktura projektu**:
  - `main.py` - główna aplikacja
  - `utils/` - algorytmy szyfrowania
  - `views/` - okna interfejsu użytkownika
  - `requirements.txt` - zależności projektu
  - `README.md` - dokumentacja projektu

### Funkcjonalności techniczne
- **Szyfr Cezara**:
  - Przesunięcie alfabetyczne (1-25)
  - Obsługa polskich znaków
  - Szyfrowanie tekstu i plików

- **Szyfr Vigenère**:
  - Klucz słowny (dowolna długość)
  - Obsługa polskich znaków
  - Szyfrowanie tekstu i plików

- **Stream Cipher**:
  - Deterministyczny strumień klucza
  - Użycie SHA-256 do generowania strumienia
  - Obsługa plików binarnych
  - Szyfrowanie XOR

- **System logowania**:
  - Logowanie wszystkich operacji
  - Informacje o użytkownikach
  - Logowanie błędów i ostrzeżeń
  - Timestampy i szczegóły operacji

---

## Typy zmian

- **Dodane** - nowe funkcjonalności
- **Zmienione** - zmiany w istniejących funkcjonalnościach
- **Przestarzałe** - funkcjonalności, które zostaną usunięte w przyszłych wersjach
- **Usunięte** - funkcjonalności usunięte w tej wersji
- **Naprawione** - poprawki błędów
- **Bezpieczeństwo** - poprawki bezpieczeństwa
