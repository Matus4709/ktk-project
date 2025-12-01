<div align="center">

# 🔐 KTK – kompletna aplikacja do nauki i demonstracji szyfrowania

Interaktywny projekt akademicki napisany w **PyQt5**, który pozwala w jednym miejscu:

🎯 generować i analizować klucze,  
🧪 szyfrować / deszyfrować teksty i pliki różnymi algorytmami,  
📋 śledzić każdy krok operacji w rozbudowanym panelu logów.

</div>

---

## Spis treści

1. [Funkcjonalności](#funkcjonalności)
2. [Dostępne algorytmy](#dostępne-algorytmy)
3. [Szybki start](#szybki-start)
4. [Używanie aplikacji](#używanie-aplikacji)
5. [Architektura projektu](#architektura-projektu)
6. [Logowanie operacji](#logowanie-operacji)
7. [Moduły specjalne (ECDH i podwójna transpozycja)](#moduły-specjalne)
8. [Testy i rozszerzenia](#testy-i-rozszerzenia)

---

## Funkcjonalności

- **Tryb tekst / plik** – użytkownik wybiera nośnik danych na pierwszym ekranie.
- **Symetryczne i asymetryczne szyfry** – od prostych ćwiczeń historycznych po AES i RSA.
- **Nowy moduł podwójnej transpozycji kolumnowej** – ręcznie zaimplementowany algorytm bez użycia bibliotek kryptograficznych.
- **Uzgadnianie klucza ECDH** – generowanie par kluczy na krzywych eliptycznych i wyprowadzanie sekretu HKDF do dalszego szyfrowania (np. AES).
- **Panel logów** – każda operacja zapisywana jest krok po kroku (opis działania, dane wejściowe, wynik).
- **Przyjazny interfejs** – ekrany pozbawione „surowych” formularzy; użytkownik prowadzi intuicyjny przewodnik.

---

## Dostępne algorytmy

| Kategoria            | Algorytm / Moduł                | Zakres                                |
|----------------------|---------------------------------|---------------------------------------|
| Klasyczne            | Cezar, Vigenère                 | Tekst + pliki (również binarne)       |
| Strumieniowe         | XOR z generatorem SHA-256       | Tekst + pliki, własny strumień klucza |
| Blokowe              | AES-128/192/256                 | Implementacja od podstaw, tekst/pliki |
| Symetryczne custom   | Podwójna transpozycja kolumnowa | Tekst (hex) + pliki (`*.dtc`)         |
| Asymetryczne         | RSA                             | Tekst + pliki                         |
| Uzgadnianie klucza   | ECDH + HKDF                     | Generowanie sekretu do szyfrów        |

---

## Szybki start

```bash
# 1. Klonuj repozytorium
git clone https://github.com/matus4709/ktk-project.git
cd ktk-project

# 2. Utwórz i aktywuj wirtualne środowisko (Python 3.11+)
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux/macOS

# 3. Doładuj zależności
pip install -r requirements.txt

# 4. Uruchom aplikację
python main.py
```

> 💡 W katalogu `requirements.txt` znajdują się zarówno zależności interfejsu (PyQt5, narzędzia Qt Designer), jak i biblioteki wspierające algorytmy (np. `cryptography` dla ECDH).

---

## Używanie aplikacji

1. **Tryb pracy** – na ekranie startowym wybierz „Szyfrowanie” lub „Deszyfrowanie”.
2. **Nośnik danych** – wskazanie „Tekst” / „Plik” otwiera okno wyboru szyfru.
3. **Wybór algorytmu** – każdy szyfr ma osobne okno z dedykowanymi polami (klucz, wejście, wynik).  
   - przy pracy na plikach dostępne są selektory ścieżek i podglądy,
   - przy pracy na tekście wynik od razu można skopiować do schowka.
4. **Logi** – przyciski „Pokaż logi / Log viewer” otwierają dedykowane okno z dokładnym przebiegiem operacji (przydatne do sprawozdań).

---

## Architektura projektu

```
ktk-project/
├── main.py                     # punkt wejścia PyQt5
├── views/                      # wszystkie okna interfejsu
│   ├── choice_window.py        # wybór trybu tekst/pliki
│   ├── cipher_choice_window.py # lista algorytmów
│   ├── encrypt_* / decrypt_*   # dedykowane okna dla każdego szyfru
│   ├── ecdh_window.py          # moduł uzgadniania klucza
│   └── log_viewer_window.py    # panel logów
├── utils/
│   ├── aes_cipher.py           # implementacja AES
│   ├── caesar_cipher.py, vigenere_cipher.py, stream_cipher.py
│   ├── rsa_cipher.py, crypto_utils.py
│   ├── double_transposition_cipher.py  # nowy moduł dwustopniowej transpozycji
│   └── logger.py               # wspólny rejestrator zdarzeń
└── requirements.txt
```

- **Warstwa `views`** odpowiada za UX (styling, walidacje formularzy, notyfikacje).
- **Warstwa `utils`** zawiera całą logikę kryptograficzną i narzędziową – każdy moduł jest gotowy do niezależnego użycia (np. w testach).
- **`logger`** zbiera kroki algorytmów, co pozwala łatwo dokumentować wyniki eksperymentów.

---

## Logowanie operacji

- Każdy moduł woła `app_logger.start_operation(...)` przed rozpoczęciem działania.
- Kolejne fazy (walidacja, generowanie klucza, transformacje) dopisują się do logu jako „STEP / INFO / SUCCESS”.
- Okno logów (`views/log_viewer_window.py`) wyświetla dane chronologicznie oraz pozwala zapisać je do pliku – świetne źródło screenów i opisów do raportu.

---

## Moduły specjalne

### 🤝 ECDH + HKDF

1. Wybór krzywej (`secp256r1`, `secp384r1`, `secp521r1`, `secp256k1`).
2. Generacja pary kluczy (PEM) – klucz publiczny można skopiować jednym kliknięciem.
3. Wczytanie/załadowanie klucza partnera z pliku i obliczenie wspólnego sekretu.
4. HKDF wyprowadza gotowy klucz symetryczny (dowolna długość 16‒64 bajtów).  
   Klucze można zapisać/wczytać z dysku, co ułatwia późniejsze użycie w module AES.

### 🧩 Podwójna transpozycja kolumnowa

- Wymaga dwóch haseł (A i B). Każde hasło określa własną kolejność kolumn.
- Tekst: dane są kodowane do UTF‑8, poprzedzane prefiksem długości, następnie dwukrotnie permutowane i zwracane jako hex.
- Pliki: otrzymują rozszerzenie `*.dtc`, a prefiks długości pozwala zachować dokładnie tę samą liczbę bajtów po odszyfrowaniu.
- Całość została zaimplementowana manualnie – bez korzystania z bibliotek kryptograficznych – co czyni moduł idealnym do omawiania na zajęciach.

---

## Testy i rozszerzenia

- **Testy ręczne** – ze względu na środowisko GUI najprostszym sposobem jest uruchomienie `python main.py` i przejście przez poszczególne okna.
- **Rozszerzanie algorytmów** – każdy szyfr posiada osobny moduł w `utils/` i odpowiadające okno w `views/`; dodanie nowego algorytmu sprowadza się do:
  1. napisania logiki w `utils/<nowy_szyfr>.py`,
  2. stworzenia okna `views/encrypt_text_<nowy>.py` / `views/decrypt_text_<nowy>.py`,
  3. zarejestrowania przycisku w `cipher_choice_window.py`.
- **Przenoszenie logiki** – biblioteki nie są „ukryte” w interfejsie, więc moduły szyfrujące można wykorzystać w skryptach CLI lub notatnikach Jupyter.

---
