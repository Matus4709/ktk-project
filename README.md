## Aplikacja szyfrująca KTK

Interfejs PyQt5 pozwalający na szyfrowanie/odszyfrowywanie tekstu i plików przy użyciu:

- klasycznych szyfrów (Cezar, Vigenère, strumieniowy),
- nowoczesnych algorytmów symetrycznych (`AES`),
- kryptografii asymetrycznej (`RSA`),
- **nowego modułu uzgadniania klucza `ECDH` (Elliptic Curve Diffie-Hellman)**.

### Moduł ECDH

Wybierz 🤝 **ECDH** w oknie wyboru szyfrów, aby:

1. wybrać jedną z krzywych eliptycznych (domyślnie `secp256r1`),
2. wygenerować klucz prywatny/publiczny (PEM),
3. wkleić klucz publiczny partnera i obliczyć surowy sekret ECDH,
4. otrzymać klucz symetryczny wyprowadzony przez HKDF (idealny do AES/HMAC).

Wszystkie operacje są szczegółowo logowane i dostępne z poziomu okna logów.

