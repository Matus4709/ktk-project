# 🔐 Aplikacja Szyfrowania/Deszyfrowania

Aplikacja desktopowa napisana w Python z wykorzystaniem PyQt5 do szyfrowania i deszyfrowania tekstu oraz plików.

## 🚀 Funkcjonalności

- **Trzy metody szyfrowania**:
  - 🔤 **Szyfr Cezara** - Klasyczny szyfr przesuwający
  - 🔑 **Szyfr Vigenère** - Szyfr polialfabetyczny z kluczem
  - 🌊 **Szyfr z kluczem bieżącym** - Stream cipher z deterministycznym strumieniem
- **Szyfrowanie tekstu i plików** - Obsługa zarówno tekstu jak i plików binarnych
- **Nowoczesny interfejs GUI** - Intuicyjny interfejs z PyQt5
- **Bezpieczne szyfrowanie** - Własne implementacje algorytmów kryptograficznych

## 📋 Wymagania

- Python 3.7+
- PyQt5

## 🛠️ Instalacja

1. Sklonuj lub pobierz projekt
2. Zainstaluj wymagane biblioteki:

```bash
pip install -r requirements.txt
```

## 🎯 Uruchomienie

```bash
python main.py
```

## 📖 Jak używać

### 1. Wybór operacji
1. Uruchom aplikację: `python main.py`
2. Wybierz **"🔒 Szyfrowanie"** lub **"🔓 Deszyfrowanie"**

### 2. Wybór typu danych
- **📝 Tekst** - dla szyfrowania/deszyfrowania tekstu
- **📁 Plik** - dla szyfrowania/deszyfrowania plików

### 3. Wybór metody szyfrowania
- **🔤 Szyfr Cezara** - przesunięcie alfabetyczne (1-25)
- **🔑 Szyfr Vigenère** - szyfr polialfabetyczny z kluczem
- **🌊 Szyfr z kluczem bieżącym** - stream cipher z deterministycznym strumieniem

### 4. Operacje na tekście
1. Wprowadź tekst do szyfrowania/deszyfrowania
2. Podaj klucz (przesunięcie/klucz/ziarno)
3. Kliknij odpowiedni przycisk
4. Skopiuj wynik przyciskiem "📋 Kopiuj wynik"

### 5. Operacje na plikach
1. Wybierz plik wejściowy
2. Wybierz lokalizację pliku wyjściowego
3. Podaj klucz
4. Kliknij przycisk szyfrowania/deszyfrowania
5. Plik zostanie zapisany w wybranej lokalizacji

## 🔧 Struktura projektu

```
ktk-project/
├── main.py                           # Główny plik aplikacji
├── requirements.txt                  # Wymagane biblioteki
├── README.md                        # Dokumentacja projektu
├── utils/                           # Algorytmy szyfrowania
│   ├── __init__.py
│   ├── caesar_cipher.py            # Szyfr Cezara
│   ├── vigenere_cipher.py          # Szyfr Vigenère
│   ├── stream_cipher.py            # Szyfr z kluczem bieżącym
│   ├── crypto_utils.py             # Funkcje pomocnicze
│   └── logger.py                   # System logowania
└── views/                           # Okna aplikacji
    ├── __init__.py
    ├── choice_window.py            # Wybór tekst/plik
    ├── cipher_choice_window.py     # Wybór metody szyfrowania
    ├── encrypt_text.py             # Szyfrowanie tekstu (Cezar)
    ├── encrypt_text_vigenere.py    # Szyfrowanie tekstu (Vigenère)
    ├── encrypt_text_stream.py      # Szyfrowanie tekstu (Stream)
    ├── encrypt_file.py             # Szyfrowanie pliku (Cezar)
    ├── encrypt_file_vigenere.py    # Szyfrowanie pliku (Vigenère)
    ├── encrypt_file_stream.py      # Szyfrowanie pliku (Stream)
    ├── decrypt_text.py             # Deszyfrowanie tekstu (Cezar)
    ├── decrypt_text_vigenere.py    # Deszyfrowanie tekstu (Vigenère)
    ├── decrypt_text_stream.py      # Deszyfrowanie tekstu (Stream)
    ├── decrypt_file.py             # Deszyfrowanie pliku (Cezar)
    ├── decrypt_file_vigenere.py   # Deszyfrowanie pliku (Vigenère)
    └── decrypt_file_stream.py      # Deszyfrowanie pliku (Stream)
```

## 🎨 Funkcje GUI

- **Główne okno** - Wybór między szyfrowaniem a deszyfrowaniem
- **Okno wyboru typu** - Wybór między tekstem a plikiem
- **Okno wyboru szyfru** - Wybór metody szyfrowania (Cezar/Vigenère/Stream)
- **Okna szyfrowania** - Dedykowane interfejsy dla każdej metody
- **Okna deszyfrowania** - Dedykowane interfejsy dla każdej metody
- **Responsywny design** - Dostosowuje się do różnych rozmiarów okien
- **Nowoczesny styl** - Gradienty, zaokrąglone rogi, ikony
- **Paski postępu** - Dla operacji na plikach
- **Informacje zwrotne** - Szczegółowe komunikaty o operacjach

## 🔒 Metody szyfrowania

### 🔤 Szyfr Cezara
- **Typ**: Szyfr przesuwający (substitution cipher)
- **Klucz**: Przesunięcie alfabetyczne (1-25)
- **Bezpieczeństwo**: Podstawowy, edukacyjny
- **Zastosowanie**: Tekst i pliki tekstowe

### 🔑 Szyfr Vigenère
- **Typ**: Szyfr polialfabetyczny
- **Klucz**: Słowo kluczowe (dowolna długość)
- **Bezpieczeństwo**: Średni, trudniejszy do złamania
- **Zastosowanie**: Tekst i pliki tekstowe

### 🌊 Szyfr z kluczem bieżącym (Stream Cipher)
- **Typ**: Szyfr strumieniowy
- **Klucz**: Ziarno (seed) do generowania strumienia
- **Bezpieczeństwo**: Wysoki, deterministyczny strumień
- **Zastosowanie**: Tekst, pliki tekstowe i binarne
- **Algorytm**: SHA-256 + XOR

