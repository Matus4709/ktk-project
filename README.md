# 🔐 Aplikacja Szyfrowania/Deszyfrowania

Aplikacja desktopowa napisana w Python z wykorzystaniem PyQt5 do szyfrowania i deszyfrowania tekstu.

## 🚀 Funkcjonalności

- **Szyfrowanie tekstu** - Bezpieczne szyfrowanie tekstu z opcjonalnym hasłem
- **Deszyfrowanie tekstu** - Odszyfrowywanie wcześniej zaszyfrowanych tekstów
- **Ładny interfejs GUI** - Nowoczesny i intuicyjny interfejs użytkownika
- **Kopiowanie wyników** - Możliwość kopiowania zaszyfrowanych/odszyfrowanych tekstów
- **Bezpieczeństwo** - Wykorzystanie biblioteki cryptography z algorytmem Fernet

## 📋 Wymagania

- Python 3.7+
- PyQt5
- cryptography

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

### Szyfrowanie
1. Kliknij przycisk "🔒 Szyfrowanie"
2. Wprowadź tekst do szyfrowania
3. Opcjonalnie wprowadź hasło
4. Kliknij "🔒 Szyfruj"
5. Skopiuj wynik przyciskiem "📋 Kopiuj wynik"

### Deszyfrowanie
1. Kliknij przycisk "🔓 Deszyfrowanie"
2. Wprowadź zaszyfrowany tekst
3. Wprowadź hasło (jeśli było używane podczas szyfrowania)
4. Kliknij "🔓 Deszyfruj"
5. Skopiuj wynik przyciskiem "📋 Kopiuj wynik"

## 🔧 Struktura projektu

```
ktk-project/
├── main.py              # Główny plik aplikacji
├── requirements.txt     # Wymagane biblioteki
└── README.md           # Ten plik
```

## 🎨 Funkcje GUI

- **Główne okno** - Wybór między szyfrowaniem a deszyfrowaniem
- **Okno szyfrowania** - Interfejs do szyfrowania tekstu
- **Okno deszyfrowania** - Interfejs do deszyfrowania tekstu
- **Responsywny design** - Dostosowuje się do różnych rozmiarów okien
- **Nowoczesny styl** - Gradienty, zaokrąglone rogi, ikony

## 🔒 Bezpieczeństwo

Aplikacja wykorzystuje:
- **Fernet** - Symetryczne szyfrowanie z autentykacją
- **Base64** - Kodowanie kluczy
- **SHA-256** - Haszowanie haseł

## 🚀 Możliwości rozbudowy

Aplikacja została zaprojektowana z myślą o dalszej rozbudowie:
- Dodanie szyfrowania plików
- Eksport/import kluczy
- Historia operacji
- Różne algorytmy szyfrowania
- Integracja z chmurą

## 👨‍💻 Autor

Python Developer - Aplikacja stworzona w ramach projektu edukacyjnego

## 📄 Licencja

Projekt edukacyjny - do użytku osobistego i naukowego
