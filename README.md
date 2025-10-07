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
├── main.py                    # Główny plik aplikacji
├── requirements.txt           # Wymagane biblioteki
├── README.md                 # Ten plik
├── utils/                    # Wspólne funkcje
│   ├── __init__.py
│   └── crypto_utils.py       # Funkcje szyfrowania/deszyfrowania
└── views/                    # Okna aplikacji
    ├── __init__.py
    ├── choice_window.py      # Okno wyboru tekst/plik
    ├── encrypt_text.py       # Okno szyfrowania tekstu
    ├── encrypt_file.py       # Okno szyfrowania pliku
    ├── decrypt_text.py       # Okno deszyfrowania tekstu
    └── decrypt_file.py       # Okno deszyfrowania pliku
```

## 🎨 Funkcje GUI

- **Główne okno** - Wybór między szyfrowaniem a deszyfrowaniem
- **Okno wyboru** - Wybór między szyfrowaniem/deszyfrowaniem tekstu a pliku
- **Okno szyfrowania tekstu** - Interfejs do szyfrowania tekstu
- **Okno szyfrowania pliku** - Interfejs do szyfrowania plików
- **Okno deszyfrowania tekstu** - Interfejs do deszyfrowania tekstu
- **Okno deszyfrowania pliku** - Interfejs do deszyfrowania plików
- **Responsywny design** - Dostosowuje się do różnych rozmiarów okien
- **Nowoczesny styl** - Gradienty, zaokrąglone rogi, ikony

## 🔒 Bezpieczeństwo

Aplikacja wykorzystuje:
- **Szyfr Cezara** - Klasyczny szyfr przesuwający
- **Własna implementacja** - Napisany od zera algorytm
- **Przesunięcie 1-25** - Konfigurowalny klucz szyfrowania

## 🔤 Algorytm Szyfru Cezara - Dokumentacja Projektowa

### 1. Historia i Podstawy Teoretyczne

**Szyfr Cezara** (łac. *Caesar cipher*) to jeden z najstarszych i najprostszych algorytmów szyfrowania, nazwany na cześć Juliusza Cezara, który podobno używał go do komunikacji wojskowej. Jest to przykład **szyfru przesuwającego** (substitution cipher), gdzie każda litera w tekście jest zastępowana literą znajdującą się o stałą liczbę pozycji dalej w alfabecie.

### 2. Zasada Działania

#### 2.1 Podstawowa Koncepcja
Szyfr Cezara działa na zasadzie **przesunięcia alfabetycznego**:
- Każda litera w tekście jest przesuwana o stałą liczbę pozycji w alfabecie
- Przesunięcie może być w zakresie 1-25 (26 pozycji to pełny obrót, więc bez efektu)
- Alfabet "zawija się" - po 'Z' następuje 'A'

#### 2.2 Matematyczny Model
```
Szyfrowanie:  E(x) = (x + k) mod 26
Deszyfrowanie: D(x) = (x - k) mod 26
```
Gdzie:
- `x` = pozycja litery w alfabecie (0-25)
- `k` = klucz (przesunięcie)
- `mod 26` = operacja modulo zapewniająca zawijanie alfabetu

### 3. Implementacja w Projekcie

#### 3.1 Struktura Algorytmu
```python
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
                # Szyfruj duże litery: A=0, B=1, ..., Z=25
                result += chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            else:
                # Szyfruj małe litery: a=0, b=1, ..., z=25
                result += chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
        else:
            # Pozostaw znaki niealfabetyczne bez zmian
            result += char
    
    return result
```

#### 3.2 Kluczowe Elementy Implementacji

**1. Walidacja Klucza:**
```python
if not isinstance(shift, int) or shift < 1 or shift > 25:
    raise ValueError("Przesunięcie musi być liczbą całkowitą od 1 do 25")
```

**2. Obsługa Wielkości Liter:**
```python
if char.isupper():
    # Dla dużych liter: A=65, B=66, ..., Z=90
    result += chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
else:
    # Dla małych liter: a=97, b=98, ..., z=122
    result += chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
```

**3. Zachowanie Znaków Niealfabetycznych:**
```python
else:
    # Znaki niealfabetyczne (spacje, cyfry, znaki specjalne) pozostają bez zmian
    result += char
```

### 4. Przykłady Działania

#### 4.1 Przykład Podstawowy
```
Tekst oryginalny: "Hello World"
Przesunięcie: 3
Proces szyfrowania:
H → K (7 + 3 = 10 → K)
e → h (4 + 3 = 7 → h)
l → o (11 + 3 = 14 → o)
l → o (11 + 3 = 14 → o)
o → r (14 + 3 = 17 → r)
(space) → (space) (znak niealfabetyczny)
W → Z (22 + 3 = 25 → Z)
o → r (14 + 3 = 17 → r)
r → u (17 + 3 = 20 → u)
l → o (11 + 3 = 14 → o)
d → g (3 + 3 = 6 → g)

Wynik: "Khoor Zruog"
```

#### 4.2 Przykład z Zawijaniem Alfabetu
```
Tekst: "XYZ"
Przesunięcie: 3
X → A (23 + 3 = 26 → 26 % 26 = 0 → A)
Y → B (24 + 3 = 27 → 27 % 26 = 1 → B)
Z → C (25 + 3 = 28 → 28 % 26 = 2 → C)

Wynik: "ABC"
```

### 5. Analiza Złożoności

#### 5.1 Złożoność Czasowa
- **O(n)** gdzie n = długość tekstu
- Każdy znak jest przetwarzany dokładnie raz
- Operacje na pojedynczym znaku są stałe O(1)

#### 5.2 Złożoność Pamięciowa
- **O(n)** dla przechowywania wyniku
- **O(1)** dodatkowej pamięci (nie licząc wyniku)

### 6. Bezpieczeństwo i Ograniczenia

#### 6.1 Słabości Algorytmu
1. **Mała przestrzeń kluczy**: Tylko 25 możliwych przesunięć
2. **Podatność na analizę częstotliwości**: Można złamać analizując częstość występowania liter
3. **Brak losowości**: Ten sam tekst z tym samym kluczem zawsze daje ten sam wynik
4. **Zachowanie wzorców**: Spacje i znaki specjalne pozostają niezmienione

#### 6.2 Metody Kryptoanalizy
1. **Brute Force**: Sprawdzenie wszystkich 25 możliwych kluczy
2. **Analiza częstotliwości**: Porównanie z typowymi częstotliwościami liter w języku
3. **Analiza wzorców**: Wykorzystanie zachowania spacji i znaków specjalnych

### 7. Zastosowania w Projekcie

#### 7.1 Funkcjonalności Zaimplementowane
- ✅ **Szyfrowanie tekstu** - interaktywne szyfrowanie w czasie rzeczywistym
- ✅ **Deszyfrowanie tekstu** - odszyfrowywanie z podglądem
- ✅ **Szyfrowanie plików** - szyfrowanie całych plików tekstowych
- ✅ **Deszyfrowanie plików** - odszyfrowywanie plików z podglądem
- ✅ **Podgląd przed zapisem** - możliwość sprawdzenia wyniku przed zapisem

#### 7.2 Interfejs Użytkownika
- **Walidacja klucza**: Sprawdzanie czy przesunięcie jest w zakresie 1-25
- **Obsługa błędów**: Informatywne komunikaty o błędach
- **Podgląd wyniku**: Możliwość zobaczenia efektu przed zapisem
- **Wielojęzyczność**: Obsługa polskich znaków (UTF-8)

### 8. Wartość Edukacyjna

#### 8.1 Cele Dydaktyczne
- **Zrozumienie podstaw kryptografii**: Jak działają szyfry podstawieniowe
- **Praktyczne zastosowanie matematyki**: Operacje modulo, arytmetyka znaków
- **Analiza bezpieczeństwa**: Zrozumienie ograniczeń prostych szyfrów
- **Programowanie**: Implementacja algorytmów kryptograficznych

#### 8.2 Umiejętności Rozwijane
- **Algorytmy i struktury danych**: Implementacja szyfrów
- **Bezpieczeństwo informacji**: Podstawy kryptografii
- **Programowanie**: Obsługa tekstu, walidacja danych
- **Interfejs użytkownika**: Tworzenie aplikacji desktopowych

### 9. Podsumowanie

Szyfr Cezara, mimo swojej prostoty, stanowi doskonały punkt wyjścia do nauki kryptografii. W projekcie został zaimplementowany jako **kompletny system szyfrowania/deszyfrowania** z interfejsem graficznym, demonstrując:

- **Teoretyczne podstawy** kryptografii
- **Praktyczną implementację** algorytmów
- **Analizę bezpieczeństwa** systemów szyfrowania
- **Tworzenie aplikacji** użytkowych

Projekt pokazuje, że nawet proste algorytmy mogą być podstawą do stworzenia funkcjonalnej aplikacji, ucząc jednocześnie podstaw bezpieczeństwa informacji i programowania.

## 📋 Changelog

### v1.0.0 - Pierwsza wersja (2024)
**🎯 Główne funkcjonalności:**
- ✅ **Okno główne** z przyciskami "Szyfrowanie" i "Deszyfrowanie"
- ✅ **Wybór typu** - tekst lub plik
- ✅ **Wybór szyfru** - okno wyboru typu szyfrowania
- ✅ **Szyfr Cezara** - pełna implementacja algorytmu
- ✅ **Interfejs graficzny** - nowoczesny design z PyQt5

### v1.1.0 - Rozbudowa interfejsu
**🎨 Ulepszenia UI:**
- ✅ **Maksymalizacja okien** - aplikacja zawsze otwiera się zmaksymalizowana
- ✅ **Poprawa layoutu** - naprawiono nachodzące się przyciski
- ✅ **Sekcje grupujące** - lepsze organizowanie elementów
- ✅ **Responsywny design** - dostosowanie do różnych rozmiarów

### v1.2.0 - Implementacja szyfrowania
**🔒 Funkcjonalności kryptograficzne:**
- ✅ **Szyfrowanie tekstu** - interaktywne szyfrowanie w czasie rzeczywistym
- ✅ **Deszyfrowanie tekstu** - odszyfrowywanie z walidacją
- ✅ **Szyfrowanie plików** - szyfrowanie całych plików tekstowych
- ✅ **Deszyfrowanie plików** - odszyfrowywanie plików z wyborem lokalizacji
- ✅ **Walidacja klucza** - sprawdzanie przesunięcia (1-25)

### v1.3.0 - Podgląd i ulepszenia
**👁️ Nowe funkcjonalności:**
- ✅ **Podgląd szyfrowania** - możliwość zobaczenia efektu przed zapisem pliku
- ✅ **Podgląd deszyfrowania** - sprawdzenie wyniku przed zapisem
- ✅ **Większe ramki informacyjne** - lepsze wyświetlanie szczegółów
- ✅ **Obsługa błędów** - informatywne komunikaty o problemach

### v1.4.0 - Dokumentacja i optymalizacja
**📚 Dokumentacja i kod:**
- ✅ **Szczegółowa dokumentacja** - kompletny opis algorytmu Cezara
- ✅ **Analiza złożoności** - O(n) czasowa i pamięciowa
- ✅ **Przykłady praktyczne** - demonstracja działania algorytmu
- ✅ **Wartość edukacyjna** - cele dydaktyczne i umiejętności

### 🔧 **Struktura projektu:**
```
ktk-project/
├── main.py                    # Główne okno aplikacji
├── requirements.txt           # Zależności projektu
├── README.md                 # Dokumentacja projektu
├── views/                    # Okna aplikacji
│   ├── __init__.py
│   ├── choice_window.py      # Wybór tekst/plik
│   ├── cipher_choice_window.py # Wybór typu szyfru
│   ├── encrypt_text.py       # Szyfrowanie tekstu
│   ├── decrypt_text.py       # Deszyfrowanie tekstu
│   ├── encrypt_file.py       # Szyfrowanie pliku
│   └── decrypt_file.py       # Deszyfrowanie pliku
└── utils/                    # Narzędzia pomocnicze
    ├── __init__.py
    └── caesar_cipher.py      # Implementacja szyfru Cezara
```

### 🎯 **Kluczowe osiągnięcia:**
- **Modularna architektura** - każdy widok w osobnym pliku
- **Własna implementacja** - algorytm napisany od zera
- **Kompletna funkcjonalność** - szyfrowanie/deszyfrowanie tekstu i plików
- **Profesjonalny interfejs** - nowoczesny design z PyQt5
- **Dokumentacja akademicka** - szczegółowy opis dla celów edukacyjnych

### 🚀 **Możliwości rozbudowy:**
- **Dodatkowe szyfry** - AES, RSA, Vigenère
- **Szyfrowanie obrazów** - steganografia
- **Klucze publiczne** - infrastruktura PKI
- **Sieciowe szyfrowanie** - komunikacja przez sieć
- **Baza danych** - przechowywanie kluczy i metadanych

## 🚀 Możliwości rozbudowy

Aplikacja została zaprojektowana z myślą o dalszej rozbudowie:
- ✅ Szyfrowanie plików (zaimplementowane)
- Eksport/import kluczy
- Historia operacji
- Różne algorytmy szyfrowania
- Integracja z chmurą
- Szyfrowanie folderów
- Automatyczne tworzenie kopii zapasowych

## 👨‍💻 Autor

Python Developer - Aplikacja stworzona w ramach projektu edukacyjnego

## 📄 Licencja

Projekt edukacyjny - do użytku osobistego i naukowego
