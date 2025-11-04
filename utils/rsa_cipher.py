"""
RSA (Rivest-Shamir-Adleman) Implementation
Implementacja szyfru RSA od podstaw bez korzystania z gotowych bibliotek
"""

import random
import hashlib
import json
import os
from typing import Tuple, Optional
from utils.logger import AppLogger

app_logger = AppLogger()


class RSA:
    """
    Implementacja szyfru RSA od podstaw
    """
    
    def __init__(self, key_size: int = 1024):
        """
        Inicjalizacja RSA
        
        Args:
            key_size: Rozmiar klucza w bitach (min 512, zalecane 1024+)
        """
        self.key_size = max(512, key_size)  # Minimum 512 bits
        app_logger.info(f"RSA initialized with {self.key_size}-bit key")
    
    def _is_prime(self, n: int, k: int = 5) -> bool:
        """
        Test pierwszości Miller-Rabin
        
        Args:
            n: Liczba do sprawdzenia
            k: Liczba iteracji testu
            
        Returns:
            True jeśli prawdopodobnie pierwsza, False w przeciwnym razie
        """
        if n < 2:
            return False
        if n == 2 or n == 3:
            return True
        if n % 2 == 0:
            return False
        
        # Zapisz n-1 jako d * 2^r
        d = n - 1
        r = 0
        while d % 2 == 0:
            d //= 2
            r += 1
        
        # Test Miller-Rabin
        for _ in range(k):
            a = random.randint(2, n - 2)
            x = pow(a, d, n)
            
            if x == 1 or x == n - 1:
                continue
            
            for _ in range(r - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    break
            else:
                return False
        
        return True
    
    def _generate_prime(self, bits: int) -> int:
        """
        Generuje losową liczbę pierwszą o określonej liczbie bitów
        
        Args:
            bits: Liczba bitów
            
        Returns:
            Liczba pierwsza
        """
        while True:
            # Generuj losową liczbę o określonej liczbie bitów
            candidate = random.getrandbits(bits)
            # Ustaw najwyższy i najniższy bit na 1 (dla nieparzystości i odpowiedniego rozmiaru)
            candidate |= (1 << (bits - 1)) | 1
            
            if self._is_prime(candidate):
                return candidate
    
    def _extended_gcd(self, a: int, b: int) -> Tuple[int, int, int]:
        """
        Rozszerzony algorytm Euklidesa
        Zwraca (gcd, x, y) takie że ax + by = gcd(a, b)
        
        Args:
            a, b: Liczby całkowite
            
        Returns:
            Tuple (gcd, x, y)
        """
        if a == 0:
            return b, 0, 1
        
        gcd, x1, y1 = self._extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        
        return gcd, x, y
    
    def _mod_inverse(self, a: int, m: int) -> int:
        """
        Oblicza odwrotność modularną a^(-1) mod m
        
        Args:
            a: Liczba
            m: Modulo
            
        Returns:
            Odwrotność modularna
        """
        gcd, x, _ = self._extended_gcd(a % m, m)
        if gcd != 1:
            raise ValueError("Odwrotność modularna nie istnieje")
        return (x % m + m) % m
    
    def generate_key_pair(self) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        """
        Generuje parę kluczy RSA (publiczny i prywatny)
        
        Returns:
            Tuple ((n, e), (n, d)) gdzie:
            - (n, e) to klucz publiczny
            - (n, d) to klucz prywatny
        """
        try:
            app_logger.info(f"Generowanie pary kluczy RSA ({self.key_size} bitów)...")
            
            # Generuj dwie liczby pierwsze
            p_bits = self.key_size // 2
            q_bits = self.key_size - p_bits
            
            p = self._generate_prime(p_bits)
            q = self._generate_prime(q_bits)
            
            # Oblicz n = p * q
            n = p * q
            
            # Oblicz funkcję Eulera φ(n) = (p-1)(q-1)
            phi_n = (p - 1) * (q - 1)
            
            # Wybierz e (publiczny wykładnik) - zwykle 65537
            e = 65537
            if e >= phi_n:
                e = 3
            
            # Sprawdź czy e i phi_n są względnie pierwsze
            while self._extended_gcd(e, phi_n)[0] != 1:
                e += 2
            
            # Oblicz d (prywatny wykładnik) - odwrotność e mod phi_n
            d = self._mod_inverse(e, phi_n)
            
            public_key = (n, e)
            private_key = (n, d)
            
            app_logger.info("Para kluczy RSA wygenerowana pomyślnie")
            return public_key, private_key
            
        except Exception as e:
            app_logger.error(f"Błąd podczas generowania kluczy RSA: {str(e)}")
            raise
    
    def encrypt_block(self, message: int, public_key: Tuple[int, int]) -> int:
        """
        Szyfruje pojedynczy blok wiadomości
        
        Args:
            message: Wiadomość jako liczba całkowita
            public_key: Klucz publiczny (n, e)
            
        Returns:
            Zaszyfrowana wiadomość
        """
        n, e = public_key
        if message < 0:
            raise ValueError("Wiadomość nie może być ujemna")
        if message >= n:
            raise ValueError(f"Wiadomość ({message}) jest zbyt duża dla klucza RSA (n={n})")
        
        return pow(message, e, n)
    
    def decrypt_block(self, ciphertext: int, private_key: Tuple[int, int]) -> int:
        """
        Deszyfruje pojedynczy blok wiadomości
        
        Args:
            ciphertext: Zaszyfrowana wiadomość
            private_key: Klucz prywatny (n, d)
            
        Returns:
            Odszyfrowana wiadomość
        """
        n, d = private_key
        return pow(ciphertext, d, n)
    
    def encrypt(self, plaintext: str, public_key: Tuple[int, int]) -> str:
        """
        Szyfruje tekst używając klucza publicznego
        
        Args:
            plaintext: Tekst do zaszyfrowania
            public_key: Klucz publiczny (n, e)
            
        Returns:
            Zaszyfrowany tekst (hex)
        """
        try:
            app_logger.info(f"RSA encryption started for text of length {len(plaintext)}")
            
            n, e = public_key
            # Oblicz maksymalny rozmiar bloku (w bajtach)
            # RSA może szyfrować wartości mniejsze niż n
            # Używamy (bit_length - 1) // 8 aby upewnić się że wartość < n
            block_size = (n.bit_length() - 1) // 8
            if block_size < 1:
                block_size = 1
            
            # Konwertuj tekst na bajty
            plaintext_bytes = plaintext.encode('utf-8')
            
            encrypted_blocks = []
            
            # Podziel na bloki i szyfruj
            for i in range(0, len(plaintext_bytes), block_size):
                block = plaintext_bytes[i:i + block_size]
                
                if not block:
                    break
                
                # Konwertuj blok na liczbę całkowitą
                message_int = int.from_bytes(block, 'big')
                
                # Sprawdź czy wiadomość nie przekracza n
                if message_int >= n:
                    raise ValueError(f"Blok wiadomości ({message_int}) jest za duży dla klucza RSA (n={n})")
                
                # Szyfruj blok
                encrypted_block = self.encrypt_block(message_int, public_key)
                
                # Konwertuj na hex (z zerem wiodącym jeśli potrzeba, aby zachować parzystość)
                hex_str = hex(encrypted_block)[2:]
                # Dodaj zero wiodące jeśli potrzeba (dla spójności z deszyfrowaniem)
                if len(hex_str) % 2 == 1:
                    hex_str = '0' + hex_str
                encrypted_blocks.append(hex_str)
            
            # Połącz wszystkie bloki
            encrypted_hex = '|'.join(encrypted_blocks)
            
            app_logger.info("RSA encryption completed successfully")
            return encrypted_hex
            
        except Exception as e:
            app_logger.error(f"RSA encryption failed: {str(e)}")
            raise
    
    def decrypt(self, ciphertext: str, private_key: Tuple[int, int]) -> str:
        """
        Deszyfruje tekst używając klucza prywatnego
        
        Args:
            ciphertext: Zaszyfrowany tekst (hex)
            private_key: Klucz prywatny (n, d)
            
        Returns:
            Odszyfrowany tekst
        """
        try:
            app_logger.info(f"RSA decryption started for ciphertext of length {len(ciphertext)}")
            
            # Podziel na bloki
            encrypted_blocks = ciphertext.split('|')
            
            decrypted_bytes = bytearray()
            
            # Maksymalny rozmiar bloku (w bajtach)
            max_block_size = (private_key[0].bit_length() - 1) // 8
            
            # Deszyfruj każdy blok
            for encrypted_hex in encrypted_blocks:
                if not encrypted_hex:
                    continue
                    
                # Konwertuj hex na liczbę całkowitą
                encrypted_int = int(encrypted_hex, 16)
                
                # Deszyfruj blok
                decrypted_int = self.decrypt_block(encrypted_int, private_key)
                
                # Oblicz rzeczywistą liczbę bajtów potrzebną do reprezentacji liczby
                if decrypted_int == 0:
                    # Specjalny przypadek dla zera
                    num_bytes = 1
                else:
                    # Oblicz minimalną liczbę bajtów potrzebną
                    num_bytes = (decrypted_int.bit_length() + 7) // 8
                
                # Konwertuj liczbę na bajty z dokładną liczbą bajtów
                decrypted_block = decrypted_int.to_bytes(num_bytes, 'big')
                
                decrypted_bytes.extend(decrypted_block)
            
            app_logger.info("RSA decryption completed successfully")
            return decrypted_bytes.decode('utf-8')
            
        except Exception as e:
            app_logger.error(f"RSA decryption failed: {str(e)}")
            raise
    
    def encrypt_file(self, input_file: str, output_file: str, public_key: Tuple[int, int]) -> bool:
        """
        Szyfruje plik używając klucza publicznego
        
        Args:
            input_file: Ścieżka do pliku wejściowego
            output_file: Ścieżka do pliku wyjściowego
            public_key: Klucz publiczny (n, e)
            
        Returns:
            True jeśli sukces, False w przeciwnym razie
        """
        try:
            app_logger.info(f"RSA file encryption started: {input_file} -> {output_file}")
            
            n, e = public_key
            block_size = (n.bit_length() - 1) // 8
            if block_size < 1:
                block_size = 1
            
            with open(input_file, 'rb') as f_in, open(output_file, 'w', encoding='utf-8') as f_out:
                total_blocks = 0
                blocks_data = []
                
                while True:
                    block = f_in.read(block_size)
                    if not block:
                        break
                    
                    # Zapamiętaj rzeczywisty rozmiar bloku (ważne dla ostatniego bloku)
                    actual_block_size = len(block)
                    
                    # Jeśli blok jest krótszy niż block_size, dopełnij zerami (dla konwersji na int)
                    if len(block) < block_size:
                        block = block + b'\x00' * (block_size - len(block))
                    
                    # Konwertuj blok na liczbę całkowitą
                    message_int = int.from_bytes(block, 'big')
                    
                    # Sprawdź czy wiadomość nie przekracza n
                    if message_int >= n:
                        app_logger.error(f"RSA file encryption: block too large ({message_int} >= {n})")
                        return False
                    
                    # Szyfruj blok
                    encrypted_block = self.encrypt_block(message_int, public_key)
                    
                    # Zapisz jako hex (z zerem wiodącym jeśli potrzeba)
                    hex_str = hex(encrypted_block)[2:]
                    if len(hex_str) % 2 == 1:
                        hex_str = '0' + hex_str
                    
                    # Zapisz rozmiar bloku i zaszyfrowane dane
                    blocks_data.append(f"{actual_block_size}:{hex_str}")
                    total_blocks += 1
                
                # Zapisz wszystkie bloki oddzielone |
                f_out.write('|'.join(blocks_data))
            
            app_logger.info("RSA file encryption completed successfully")
            return True
            
        except Exception as e:
            app_logger.error(f"RSA file encryption failed: {str(e)}")
            return False
    
    def decrypt_file(self, input_file: str, output_file: str, private_key: Tuple[int, int]) -> bool:
        """
        Deszyfruje plik używając klucza prywatnego
        
        Args:
            input_file: Ścieżka do pliku wejściowego
            output_file: Ścieżka do pliku wyjściowego
            private_key: Klucz prywatny (n, d)
            
        Returns:
            True jeśli sukces, False w przeciwnym razie
        """
        try:
            app_logger.info(f"RSA file decryption started: {input_file} -> {output_file}")
            
            n, d = private_key
            # Maksymalny rozmiar bloku (w bajtach) - musi być taki sam jak przy szyfrowaniu
            max_block_size = (n.bit_length() - 1) // 8
            if max_block_size < 1:
                max_block_size = 1
            
            with open(input_file, 'r', encoding='utf-8') as f_in, open(output_file, 'wb') as f_out:
                content = f_in.read()
                encrypted_blocks = content.split('|')
                
                # Usuń ostatni pusty element jeśli istnieje
                if encrypted_blocks and encrypted_blocks[-1] == '':
                    encrypted_blocks = encrypted_blocks[:-1]
                
                for block_data in encrypted_blocks:
                    if not block_data:
                        continue
                    
                    # Sprawdź czy blok ma zapisany rozmiar (nowy format) czy nie (stary format)
                    if ':' in block_data:
                        # Nowy format: "rozmiar:hex"
                        actual_block_size_str, encrypted_hex = block_data.split(':', 1)
                        actual_block_size = int(actual_block_size_str)
                    else:
                        # Stary format: tylko hex (dla kompatybilności)
                        encrypted_hex = block_data
                        actual_block_size = max_block_size
                    
                    # Konwertuj hex na liczbę całkowitą
                    encrypted_int = int(encrypted_hex, 16)
                    
                    # Deszyfruj blok
                    decrypted_int = self.decrypt_block(encrypted_int, private_key)
                    
                    # Konwertuj na bajty z pełnym rozmiarem bloku
                    decrypted_block = decrypted_int.to_bytes(max_block_size, 'big')
                    
                    # Zapisz tylko rzeczywistą liczbę bajtów (ważne dla ostatniego bloku!)
                    f_out.write(decrypted_block[:actual_block_size])
            
            app_logger.info("RSA file decryption completed successfully")
            return True
            
        except Exception as e:
            app_logger.error(f"RSA file decryption failed: {str(e)}")
            return False


# Funkcje pomocnicze dla interfejsu
def rsa_generate_key_pair(key_size: int = 1024) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    """
    Generuje parę kluczy RSA
    
    Args:
        key_size: Rozmiar klucza w bitach
        
    Returns:
        Tuple (public_key, private_key)
    """
    rsa = RSA(key_size)
    return rsa.generate_key_pair()


def rsa_encrypt_text(text: str, public_key: Tuple[int, int], key_size: int = 1024) -> str:
    """
    Szyfruje tekst RSA
    
    Args:
        text: Tekst do zaszyfrowania
        public_key: Klucz publiczny (n, e)
        key_size: Rozmiar klucza (ignorowany, używany z klucza)
        
    Returns:
        Zaszyfrowany tekst (hex)
    """
    rsa = RSA(key_size)
    return rsa.encrypt(text, public_key)


def rsa_decrypt_text(ciphertext: str, private_key: Tuple[int, int], key_size: int = 1024) -> str:
    """
    Deszyfruje tekst RSA
    
    Args:
        ciphertext: Zaszyfrowany tekst (hex)
        private_key: Klucz prywatny (n, d)
        key_size: Rozmiar klucza (ignorowany, używany z klucza)
        
    Returns:
        Odszyfrowany tekst
    """
    rsa = RSA(key_size)
    return rsa.decrypt(ciphertext, private_key)


def rsa_encrypt_file(input_file: str, output_file: str, public_key: Tuple[int, int], key_size: int = 1024) -> bool:
    """
    Szyfruje plik RSA
    
    Args:
        input_file: Ścieżka do pliku wejściowego
        output_file: Ścieżka do pliku wyjściowego
        public_key: Klucz publiczny (n, e)
        key_size: Rozmiar klucza (ignorowany, używany z klucza)
        
    Returns:
        True jeśli sukces, False w przeciwnym razie
    """
    rsa = RSA(key_size)
    return rsa.encrypt_file(input_file, output_file, public_key)


def rsa_decrypt_file(input_file: str, output_file: str, private_key: Tuple[int, int], key_size: int = 1024) -> bool:
    """
    Deszyfruje plik RSA
    
    Args:
        input_file: Ścieżka do pliku wejściowego
        output_file: Ścieżka do pliku wyjściowego
        private_key: Klucz prywatny (n, d)
        key_size: Rozmiar klucza (ignorowany, używany z klucza)
        
    Returns:
        True jeśli sukces, False w przeciwnym razie
    """
    rsa = RSA(key_size)
    return rsa.decrypt_file(input_file, output_file, private_key)


def rsa_save_key_pair(public_key: Tuple[int, int], private_key: Tuple[int, int], 
                      file_path: str, key_size: Optional[int] = None) -> bool:
    """
    Zapisuje parę kluczy RSA do pliku JSON
    
    Args:
        public_key: Klucz publiczny (n, e)
        private_key: Klucz prywatny (n, d)
        file_path: Ścieżka do pliku zapisu
        key_size: Opcjonalny rozmiar klucza do zapisania
        
    Returns:
        True jeśli sukces, False w przeciwnym razie
    """
    try:
        app_logger.info(f"RSA saving key pair to {file_path}")
        
        key_data = {
            "key_size": key_size if key_size else public_key[0].bit_length(),
            "public_key": {
                "n": str(public_key[0]),
                "e": str(public_key[1])
            },
            "private_key": {
                "n": str(private_key[0]),
                "d": str(private_key[1])
            }
        }
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(key_data, f, indent=2)
        
        app_logger.info("RSA key pair saved successfully")
        return True
        
    except Exception as e:
        app_logger.error(f"RSA key pair save failed: {str(e)}")
        return False


def rsa_save_public_key(public_key: Tuple[int, int], file_path: str, 
                       key_size: Optional[int] = None) -> bool:
    """
    Zapisuje tylko klucz publiczny RSA do pliku JSON
    
    Args:
        public_key: Klucz publiczny (n, e)
        file_path: Ścieżka do pliku zapisu
        key_size: Opcjonalny rozmiar klucza do zapisania
        
    Returns:
        True jeśli sukces, False w przeciwnym razie
    """
    try:
        app_logger.info(f"RSA saving public key to {file_path}")
        
        key_data = {
            "key_size": key_size if key_size else public_key[0].bit_length(),
            "public_key": {
                "n": str(public_key[0]),
                "e": str(public_key[1])
            }
        }
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(key_data, f, indent=2)
        
        app_logger.info("RSA public key saved successfully")
        return True
        
    except Exception as e:
        app_logger.error(f"RSA public key save failed: {str(e)}")
        return False


def rsa_save_private_key(private_key: Tuple[int, int], file_path: str, 
                        key_size: Optional[int] = None) -> bool:
    """
    Zapisuje tylko klucz prywatny RSA do pliku JSON
    
    Args:
        private_key: Klucz prywatny (n, d)
        file_path: Ścieżka do pliku zapisu
        key_size: Opcjonalny rozmiar klucza do zapisania
        
    Returns:
        True jeśli sukces, False w przeciwnym razie
    """
    try:
        app_logger.info(f"RSA saving private key to {file_path}")
        
        key_data = {
            "key_size": key_size if key_size else private_key[0].bit_length(),
            "private_key": {
                "n": str(private_key[0]),
                "d": str(private_key[1])
            }
        }
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(key_data, f, indent=2)
        
        app_logger.info("RSA private key saved successfully")
        return True
        
    except Exception as e:
        app_logger.error(f"RSA private key save failed: {str(e)}")
        return False


def rsa_load_key_pair(file_path: str) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
    """
    Ładuje parę kluczy RSA z pliku JSON
    
    Args:
        file_path: Ścieżka do pliku z kluczami
        
    Returns:
        Tuple (public_key, private_key) lub None w przypadku błędu
    """
    try:
        app_logger.info(f"RSA loading key pair from {file_path}")
        
        if not os.path.exists(file_path):
            app_logger.error(f"RSA key file not found: {file_path}")
            return None
        
        with open(file_path, 'r', encoding='utf-8') as f:
            key_data = json.load(f)
        
        # Sprawdź czy plik zawiera oba klucze
        if "public_key" not in key_data or "private_key" not in key_data:
            app_logger.error("RSA key file missing public or private key")
            return None
        
        public_key = (int(key_data["public_key"]["n"]), int(key_data["public_key"]["e"]))
        private_key = (int(key_data["private_key"]["n"]), int(key_data["private_key"]["d"]))
        
        app_logger.info("RSA key pair loaded successfully")
        return (public_key, private_key)
        
    except Exception as e:
        app_logger.error(f"RSA key pair load failed: {str(e)}")
        return None


def rsa_load_public_key(file_path: str) -> Optional[Tuple[int, int]]:
    """
    Ładuje tylko klucz publiczny RSA z pliku JSON
    
    Args:
        file_path: Ścieżka do pliku z kluczem
        
    Returns:
        Klucz publiczny (n, e) lub None w przypadku błędu
    """
    try:
        app_logger.info(f"RSA loading public key from {file_path}")
        
        if not os.path.exists(file_path):
            app_logger.error(f"RSA key file not found: {file_path}")
            return None
        
        with open(file_path, 'r', encoding='utf-8') as f:
            key_data = json.load(f)
        
        if "public_key" not in key_data:
            app_logger.error("RSA key file missing public key")
            return None
        
        public_key = (int(key_data["public_key"]["n"]), int(key_data["public_key"]["e"]))
        
        app_logger.info("RSA public key loaded successfully")
        return public_key
        
    except Exception as e:
        app_logger.error(f"RSA public key load failed: {str(e)}")
        return None


def rsa_load_private_key(file_path: str) -> Optional[Tuple[int, int]]:
    """
    Ładuje tylko klucz prywatny RSA z pliku JSON
    
    Args:
        file_path: Ścieżka do pliku z kluczem
        
    Returns:
        Klucz prywatny (n, d) lub None w przypadku błędu
    """
    try:
        app_logger.info(f"RSA loading private key from {file_path}")
        
        if not os.path.exists(file_path):
            app_logger.error(f"RSA key file not found: {file_path}")
            return None
        
        with open(file_path, 'r', encoding='utf-8') as f:
            key_data = json.load(f)
        
        if "private_key" not in key_data:
            app_logger.error("RSA key file missing private key")
            return None
        
        private_key = (int(key_data["private_key"]["n"]), int(key_data["private_key"]["d"]))
        
        app_logger.info("RSA private key loaded successfully")
        return private_key
        
    except Exception as e:
        app_logger.error(f"RSA private key load failed: {str(e)}")
        return None

