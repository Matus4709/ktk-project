## 1. Wprowadzenie i cel pracy
Niniejszy dokument stanowi techniczną dokumentację projektową aplikacji KTK – desktopowego narzędzia edukacyjnego służącego do demonstracji oraz analizy algorytmów szyfrowania tekstów i plików. Celem pracy jest:
- przedstawienie założeń i architektury rozwiązania,
- omówienie użytych technologii i wybranych algorytmów kryptograficznych,
- zaprezentowanie sposobu obsługi i walidacji danych,
- udokumentowanie historii zmian oraz wniosków wynikających z implementacji.

## 2. Kontekst i motywacja
Projekt powstał jako narzędzie dydaktyczne na zajęcia akademickie z bezpieczeństwa informacji i kryptografii stosowanej. Założono, że aplikacja:
- pozwala użytkownikowi prześledzić krok po kroku przebieg operacji kryptograficznych,
- oferuje zarówno klasyczne szyfry historyczne, jak i nowoczesne prymitywy (AES, RSA, ECDH+HKDF),
- udostępnia spójny interfejs graficzny w PyQt5 oraz bogaty moduł logowania,
- może być łatwo rozszerzana o nowe algorytmy dzięki modularnej architekturze.

## 3. Zakres funkcjonalny
- Szyfrowanie i deszyfrowanie tekstów oraz plików z wykorzystaniem wielu algorytmów.
- Generowanie i analiza par kluczy (RSA, ECDH), wyprowadzanie kluczy symetrycznych (HKDF).
- Eksport/import kluczy (RSA, ECDH) oraz wyników (hex/binarne pliki wyjściowe).
- Rejestrowanie szczegółowych logów przebiegu operacji i prezentacja w dedykowanym oknie.
- Walidacja danych wejściowych (klucze, format hex, długości, puste pola).

## 4. Technologie i środowisko uruchomieniowe
- Język: Python 3.11+
- GUI: PyQt5 (biblioteka Qt)
- Kryptografia: własne implementacje AES, RSA, szyfru strumieniowego, Cezara, Vigenère, podwójnej transpozycji kolumnowej; biblioteka `cryptography` dla ECDH+HKDF.
- Logowanie: moduł `utils/logger.py`.
- Zarządzanie zależnościami: `requirements.txt`.
- Systemy docelowe: Windows / Linux / macOS.
- Uruchamianie: `python main.py` po instalacji zależności (`pip install -r requirements.txt`).

## 5. Architektura systemu
### 5.1 Struktura katalogów (logiczny podział)
- `main.py` – punkt wejścia, uruchomienie głównego okna aplikacji.
- `views/` – warstwa prezentacji (PyQt5): okna wyboru trybu, wyboru algorytmów, okna szyfrowania/deszyfrowania dla poszczególnych szyfrów, moduł ECDH oraz przeglądarka logów.
- `utils/` – warstwa logiki kryptograficznej i narzędziowej: implementacje algorytmów, funkcje pomocnicze, logger.
- `requirements.txt` – zależności środowiskowe.

### 5.2 Warstwy i odpowiedzialności
- Prezentacja (`views`): interakcja z użytkownikiem, walidacje wejść na poziomie UI, komunikaty błędów, obsługa plików (dialogi wyboru).
- Logika (`utils`): czyste funkcje/klasy implementujące algorytmy szyfrujące, niezależne od interfejsu, możliwe do ponownego użycia w testach lub skryptach CLI.
- Infrastruktura (logowanie): spójne logowanie startu, kroków pośrednich, sukcesów i błędów; dane są dostępne z poziomu `log_viewer_window.py`.

## 6. Opis zastosowanych algorytmów
### 6.1 AES (Advanced Encryption Standard) – `utils/aes_cipher.py`
- Własna implementacja AES-128/192/256.
- Transformacje rdzeniowe: SubBytes (S-Box), ShiftRows, MixColumns (GF(2^8)), AddRoundKey.
- Generowanie kluczy rund (key schedule) z wykorzystaniem stałych Rcon; liczba rund zależna od długości klucza (10/12/14).
- Padding PKCS#7; praca na bloku 16 bajtów; konwersje bajty ↔ macierz stanu 4×4.
- Zastosowanie: szyfrowanie/deszyfrowanie tekstów i plików.

### 6.2      – `utils/rsa_cipher.py`
- Pełna implementacja algorytmu asymetrycznego: test pierwszości Miller–Rabina, generacja liczb pierwszych p i q, obliczanie φ(n), dobór wykładnika e (domyślnie 65537) oraz obliczanie d (odwrotność modularna).
- Szyfrowanie i deszyfrowanie blokowe na liczbach całkowitych; weryfikacje rozmiaru bloku względem modułu n.
- Eksport i import kluczy w formacie JSON; możliwość użycia w GUI i poza nim.

### 6.3 Szyfr strumieniowy (XOR + SHA-256 PRG) – `utils/stream_cipher.py`
- Deterministyczny generator strumienia klucza: SHA-256(seed‖counter).
- Operacja XOR między strumieniem a danymi (tekst, pliki).
- Prosty, edukacyjny model PRG; brak IV i losowości – przeznaczenie dydaktyczne, nieprodukcyjne.

### 6.4 Podwójna transpozycja kolumnowa – `utils/double_transposition_cipher.py`
- Dwa klucze literowe → wyznaczanie kolejności kolumn przez sortowanie znaków (z zachowaniem stabilności indeksów).
- Dwuetapowa permutacja kolumn (A, potem B). Padding zerowy wypełniający ostatni wiersz.
- Tekst: prefiks długości (8 bajtów) + UTF-8 → wynik w hex.
- Pliki: prefiks długości + dane binarne → wynik binarny `.dtc`.
- Zastosowanie: pokaz klasycznego szyfru transpozycyjnego i konsekwencji permutacji.

### 6.5 Cezar, Vigenère – `utils/caesar_cipher.py`, `utils/vigenere_cipher.py`
- Klasyczne szyfry podstawieniowe / polialfabetyczne.
- Obsługa tekstów i plików; walidacje klucza (niepusty, właściwy zakres).

### 6.6 ECDH + HKDF – `utils/ecdh.py`
- Wymiana klucza na krzywych eliptycznych (SECP256R1, SECP384R1, SECP521R1, SECP256K1) z wykorzystaniem biblioteki `cryptography`.
- Generacja par kluczy (PEM), obliczenie wspólnego sekretu, derivacja klucza symetrycznego przy użyciu HKDF (SHA-256, konfigurowalna długość wyjścia).
- Zastosowanie: realistyczny etap uzgadniania klucza dla szyfrów symetrycznych (np. AES).

## 7. Przepływ działania aplikacji
1) Uruchomienie `main.py` → główne okno (wybór: szyfrowanie / deszyfrowanie).  
2) Wybór nośnika danych: tekst lub plik.  
3) Wybór algorytmu: lista dostępnych szyfrów, w tym moduły specjalne (ECDH, podwójna transpozycja).  
4) Okno algorytmu: pola wejściowe na dane i klucze, przyciski akcji (szyfruj/deszyfruj), komunikaty i walidacje.  
5) Rejestracja kroków: każda operacja rozpoczyna się `start_operation`, kolejne etapy logowane jako `STEP/INFO/SUCCESS/ERROR`.  
6) Podgląd logów: `log_viewer_window.py` prezentuje sekwencję zdarzeń; logi mogą być użyte w sprawozdaniu (zrzuty ekranu).  
7) Zapis wyników: tekst (hex) lub plik wynikowy; klucze (RSA, ECDH) w formacie PEM/JSON zgodnie z modułem.

## 8. Walidacja i obsługa błędów
- Spójne sprawdzanie pustych pól, niepoprawnych formatów (np. hex), minimalnych długości kluczy (transpozycja), poprawności zakresów (RSA – wielkość bloku vs. n).
- Komunikaty błędów prezentowane użytkownikowi; równoległe logowanie szczegółów w loggerze.
- Wyjątki w logice `utils/*` przechwytywane na poziomie GUI i sygnalizowane w oknie.

## 9. Instrukcja instalacji i uruchomienia
```
git clone https://github.com/matus4709/ktk-project.git
cd ktk-project
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/macOS
pip install -r requirements.txt
python main.py
```
Wymagania: Python 3.11+, środowisko z możliwością instalacji PyQt5 i biblioteki `cryptography`.

## 10. Bezpieczeństwo i ograniczenia
- Implementacje AES/RSA są edukacyjne: brak zabezpieczeń przed atakami bocznokanałowymi, brak standardowych paddingów RSA (OAEP), brak trybów blokowych z IV/nonce (CBC/GCM) w AES – należy traktować jako materiał do nauki, nie do użytku produkcyjnego.
- Szyfr strumieniowy używa deterministycznego PRG bez IV; ten sam seed → ten sam strumień.
- Podwójna transpozycja to szyfr historyczny o ograniczonej sile bezpieczeństwa.
- Brak bezpiecznego magazynu kluczy; klucze przechowywane w plikach PEM/JSON wskazanych przez użytkownika.
- Aplikacja pracuje na plikach użytkownika bez piaskownicy – odpowiedzialność za ścieżki i uprawnienia leży po stronie użytkownika.

## 11. Testowanie
### 11.1 Testy manualne (GUI)
- Teksty: krótkie/średnie ciągi, znaki diakrytyczne, puste wejście.
- Pliki: małe binaria, różne rozszerzenia; weryfikacja integralności po deszyfracji (porównanie hash SHA-256).
- ECDH: wymiana kluczy pomiędzy dwiema instancjami aplikacji, porównanie wyprowadzonego sekretu i klucza HKDF.

### 11.2 Rekomendacje dla testów automatycznych
- Jednostkowe dla `utils/*`: porównanie wyników AES/RSA z wzorcami (np. z biblioteki `cryptography`), property-based testy dla transpozycji i PRG.
- Testy integralności plików po szyfrowaniu/deszyfrowaniu.
- Testy walidacji wejść (błędne klucze, pusty seed, nieprawidłowy hex).

## 12. Wyniki (miejsce na zrzuty ekranu)
Wstaw poniżej własne zrzuty ekranu z opisami (1–2 zdania każdy):
- Ekran startowy: wybór trybu szyfrowanie/deszyfrowanie.
- Okno AES (tekst): parametry, klucz, wynik, fragment logu.
- Okno RSA (plik): wybór pliku, klucze, status operacji.
- Moduł ECDH: para kluczy PEM, wyprowadzony klucz HKDF.
- Log viewer: sekwencja kroków dla przykładowej operacji.

## 13. Change log
- v1.0: Cezar, Vigenère (tekst/plik).
- v1.1: Szyfr strumieniowy (XOR+SHA-256), panel logów.
- v1.2: Własny AES 128/192/256, obsługa plików.
- v1.3: Własny RSA, generacja kluczy, eksport/import.
- v1.4: ECDH + HKDF (uzgadnianie klucza).
- v1.5: Podwójna transpozycja kolumnowa, rozszerzenie `.dtc`.
- v1.6: Usprawnienia UI, walidacje, rozbudowa log viewer.

## 14. Wnioski
- Projekt spełnia cele dydaktyczne: pozwala prześledzić wewnętrzne etapy szyfrowania i deszyfrowania, obserwować działanie klasycznych i współczesnych prymitywów oraz proces uzgadniania klucza (ECDH + HKDF).
- Modularna architektura (warstwa `utils` + `views`) umożliwia łatwe dodawanie kolejnych algorytmów: implementacja w `utils/<nowy_alg>.py`, okna w `views/encrypt_*/decrypt_*`, rejestracja w `cipher_choice_window.py`.
- Własne implementacje kryptograficzne są przejrzyste, lecz nieoptymalne i bez zabezpieczeń produkcyjnych; do zastosowań rzeczywistych należy stosować sprawdzone biblioteki, bezpieczne paddingi i tryby pracy (np. OAEP dla RSA, GCM dla AES).
- Kierunki rozwoju: testy automatyczne (unit/property), tryb CLI do pracy wsadowej, porównania z implementacjami referencyjnymi (`cryptography`) oraz dodanie trybów blokowych AES z IV/nonce dla celów porównawczych.

