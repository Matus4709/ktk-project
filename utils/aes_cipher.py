"""
AES (Advanced Encryption Standard) Implementation
Implementacja szyfru AES od podstaw bez korzystania z gotowych bibliotek
"""

import os
import hashlib
from typing import List, Tuple
from utils.logger import AppLogger

app_logger = AppLogger()

class AES:
    """
    Implementacja szyfru AES-128/192/256 od podstaw
    """
    
    # S-box dla transformacji SubBytes
    S_BOX = [
        0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
        0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
        0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
        0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
        0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
        0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
        0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
        0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
        0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
        0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
        0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
        0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
        0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
        0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
        0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
        0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
    ]
    
    # Odwrotny S-box dla deszyfrowania
    INV_S_BOX = [
        0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb,
        0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb,
        0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e,
        0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25,
        0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92,
        0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84,
        0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06,
        0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b,
        0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73,
        0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e,
        0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b,
        0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4,
        0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f,
        0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef,
        0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61,
        0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d
    ]
    
    # Rcon (Round Constants) dla rozszerzania klucza
    RCON = [
        0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36
    ]
    
    def __init__(self, key_size: int = 128):
        """
        Inicjalizacja AES
        
        Args:
            key_size: Rozmiar klucza w bitach (128, 192, 256)
        """
        self.key_size = key_size
        self.n_rounds = {128: 10, 192: 12, 256: 14}[key_size]
        self.n_key_words = {128: 4, 192: 6, 256: 8}[key_size]
        
        app_logger.info(f"AES initialized with {key_size}-bit key, {self.n_rounds} rounds")
    
    def _pad_data(self, data: bytes) -> bytes:
        """
        Padding PKCS#7 dla danych
        
        Args:
            data: Dane do paddingu
            
        Returns:
            Dane z paddingiem
        """
        padding_length = 16 - (len(data) % 16)
        padding = bytes([padding_length] * padding_length)
        return data + padding
    
    def _unpad_data(self, data: bytes) -> bytes:
        """
        Usuwanie paddingu PKCS#7
        
        Args:
            data: Dane z paddingiem
            
        Returns:
            Dane bez paddingu
        """
        padding_length = data[-1]
        return data[:-padding_length]
    
    def _bytes_to_matrix(self, data: bytes) -> List[List[int]]:
        """
        Konwersja bajtów na macierz 4x4
        
        Args:
            data: 16 bajtów danych
            
        Returns:
            Macierz 4x4
        """
        matrix = [[0 for _ in range(4)] for _ in range(4)]
        for i in range(4):
            for j in range(4):
                matrix[j][i] = data[i * 4 + j]
        return matrix
    
    def _matrix_to_bytes(self, matrix: List[List[int]]) -> bytes:
        """
        Konwersja macierzy 4x4 na bajty
        
        Args:
            matrix: Macierz 4x4
            
        Returns:
            16 bajtów
        """
        data = bytearray(16)
        for i in range(4):
            for j in range(4):
                data[i * 4 + j] = matrix[j][i]
        return bytes(data)
    
    def _sub_bytes(self, state: List[List[int]]) -> List[List[int]]:
        """
        Transformacja SubBytes
        
        Args:
            state: Stan AES (macierz 4x4)
            
        Returns:
            Stan po transformacji SubBytes
        """
        for i in range(4):
            for j in range(4):
                state[i][j] = self.S_BOX[state[i][j]]
        return state
    
    def _inv_sub_bytes(self, state: List[List[int]]) -> List[List[int]]:
        """
        Odwrotna transformacja SubBytes
        
        Args:
            state: Stan AES (macierz 4x4)
            
        Returns:
            Stan po odwrotnej transformacji SubBytes
        """
        for i in range(4):
            for j in range(4):
                state[i][j] = self.INV_S_BOX[state[i][j]]
        return state
    
    def _shift_rows(self, state: List[List[int]]) -> List[List[int]]:
        """
        Transformacja ShiftRows
        
        Args:
            state: Stan AES (macierz 4x4)
            
        Returns:
            Stan po transformacji ShiftRows
        """
        # Wiersz 0: bez przesunięcia
        # Wiersz 1: przesunięcie o 1 w lewo
        state[1] = state[1][1:] + state[1][:1]
        # Wiersz 2: przesunięcie o 2 w lewo
        state[2] = state[2][2:] + state[2][:2]
        # Wiersz 3: przesunięcie o 3 w lewo
        state[3] = state[3][3:] + state[3][:3]
        return state
    
    def _inv_shift_rows(self, state: List[List[int]]) -> List[List[int]]:
        """
        Odwrotna transformacja ShiftRows
        
        Args:
            state: Stan AES (macierz 4x4)
            
        Returns:
            Stan po odwrotnej transformacji ShiftRows
        """
        # Wiersz 0: bez przesunięcia
        # Wiersz 1: przesunięcie o 1 w prawo
        state[1] = state[1][-1:] + state[1][:-1]
        # Wiersz 2: przesunięcie o 2 w prawo
        state[2] = state[2][-2:] + state[2][:-2]
        # Wiersz 3: przesunięcie o 3 w prawo
        state[3] = state[3][-3:] + state[3][:-3]
        return state
    
    def _galois_multiply(self, a: int, b: int) -> int:
        """
        Mnożenie w polu Galois GF(2^8)
        
        Args:
            a, b: Wartości do pomnożenia
            
        Returns:
            Wynik mnożenia w GF(2^8)
        """
        result = 0
        for i in range(8):
            if b & 1:
                result ^= a
            a <<= 1
            if a & 0x100:
                a ^= 0x11b  # Redukcja modulo x^8 + x^4 + x^3 + x + 1
            b >>= 1
        return result & 0xff
    
    def _mix_columns(self, state: List[List[int]]) -> List[List[int]]:
        """
        Transformacja MixColumns
        
        Args:
            state: Stan AES (macierz 4x4)
            
        Returns:
            Stan po transformacji MixColumns
        """
        for i in range(4):
            s0 = state[0][i]
            s1 = state[1][i]
            s2 = state[2][i]
            s3 = state[3][i]
            
            state[0][i] = self._galois_multiply(0x02, s0) ^ self._galois_multiply(0x03, s1) ^ s2 ^ s3
            state[1][i] = s0 ^ self._galois_multiply(0x02, s1) ^ self._galois_multiply(0x03, s2) ^ s3
            state[2][i] = s0 ^ s1 ^ self._galois_multiply(0x02, s2) ^ self._galois_multiply(0x03, s3)
            state[3][i] = self._galois_multiply(0x03, s0) ^ s1 ^ s2 ^ self._galois_multiply(0x02, s3)
        
        return state
    
    def _inv_mix_columns(self, state: List[List[int]]) -> List[List[int]]:
        """
        Odwrotna transformacja MixColumns
        
        Args:
            state: Stan AES (macierz 4x4)
            
        Returns:
            Stan po odwrotnej transformacji MixColumns
        """
        for i in range(4):
            s0 = state[0][i]
            s1 = state[1][i]
            s2 = state[2][i]
            s3 = state[3][i]
            
            state[0][i] = self._galois_multiply(0x0e, s0) ^ self._galois_multiply(0x0b, s1) ^ self._galois_multiply(0x0d, s2) ^ self._galois_multiply(0x09, s3)
            state[1][i] = self._galois_multiply(0x09, s0) ^ self._galois_multiply(0x0e, s1) ^ self._galois_multiply(0x0b, s2) ^ self._galois_multiply(0x0d, s3)
            state[2][i] = self._galois_multiply(0x0d, s0) ^ self._galois_multiply(0x09, s1) ^ self._galois_multiply(0x0e, s2) ^ self._galois_multiply(0x0b, s3)
            state[3][i] = self._galois_multiply(0x0b, s0) ^ self._galois_multiply(0x0d, s1) ^ self._galois_multiply(0x09, s2) ^ self._galois_multiply(0x0e, s3)
        
        return state
    
    def _add_round_key(self, state: List[List[int]], round_key: List[List[int]]) -> List[List[int]]:
        """
        Transformacja AddRoundKey
        
        Args:
            state: Stan AES (macierz 4x4)
            round_key: Klucz rundy (macierz 4x4)
            
        Returns:
            Stan po transformacji AddRoundKey
        """
        for i in range(4):
            for j in range(4):
                state[i][j] ^= round_key[i][j]
        return state
    
    def _key_expansion(self, key: bytes) -> List[List[List[int]]]:
        """
        Rozszerzanie klucza AES
        
        Args:
            key: Klucz wejściowy
            
        Returns:
            Lista kluczy rund
        """
        key_words = []
        for i in range(0, len(key), 4):
            word = [key[i], key[i+1], key[i+2], key[i+3]]
            key_words.append(word)
        
        # Generowanie dodatkowych słów klucza
        for i in range(self.n_key_words, 4 * (self.n_rounds + 1)):
            temp = key_words[i-1][:]
            
            if i % self.n_key_words == 0:
                # RotWord
                temp = temp[1:] + temp[:1]
                # SubWord
                temp = [self.S_BOX[b] for b in temp]
                # XOR z Rcon
                temp[0] ^= self.RCON[i // self.n_key_words - 1]
            elif self.n_key_words > 6 and i % self.n_key_words == 4:
                # SubWord dla AES-256
                temp = [self.S_BOX[b] for b in temp]
            
            # XOR z słowem sprzed n_key_words
            new_word = [key_words[i-self.n_key_words][j] ^ temp[j] for j in range(4)]
            key_words.append(new_word)
        
        # Konwersja na klucze rund
        round_keys = []
        for i in range(self.n_rounds + 1):
            round_key = [[0 for _ in range(4)] for _ in range(4)]
            for j in range(4):
                for k in range(4):
                    round_key[k][j] = key_words[i*4 + j][k]
            round_keys.append(round_key)
        
        return round_keys
    
    def _encrypt_block(self, block: bytes, round_keys: List[List[List[int]]]) -> bytes:
        """
        Szyfrowanie pojedynczego bloku AES
        
        Args:
            block: 16-bajtowy blok do zaszyfrowania
            round_keys: Klucze rund
            
        Returns:
            Zaszyfrowany blok
        """
        state = self._bytes_to_matrix(block)
        
        # AddRoundKey (pierwsza runda)
        state = self._add_round_key(state, round_keys[0])
        
        # Rundy główne
        for round_num in range(1, self.n_rounds):
            state = self._sub_bytes(state)
            state = self._shift_rows(state)
            state = self._mix_columns(state)
            state = self._add_round_key(state, round_keys[round_num])
        
        # Ostatnia runda (bez MixColumns)
        state = self._sub_bytes(state)
        state = self._shift_rows(state)
        state = self._add_round_key(state, round_keys[self.n_rounds])
        
        return self._matrix_to_bytes(state)
    
    def _decrypt_block(self, block: bytes, round_keys: List[List[List[int]]]) -> bytes:
        """
        Deszyfrowanie pojedynczego bloku AES
        
        Args:
            block: 16-bajtowy blok do deszyfrowania
            round_keys: Klucze rund
            
        Returns:
            Odszyfrowany blok
        """
        state = self._bytes_to_matrix(block)
        
        # AddRoundKey (ostatnia runda)
        state = self._add_round_key(state, round_keys[self.n_rounds])
        
        # Odwrotne rundy główne
        for round_num in range(self.n_rounds - 1, 0, -1):
            state = self._inv_shift_rows(state)
            state = self._inv_sub_bytes(state)
            state = self._add_round_key(state, round_keys[round_num])
            state = self._inv_mix_columns(state)
        
        # Pierwsza runda (bez InvMixColumns)
        state = self._inv_shift_rows(state)
        state = self._inv_sub_bytes(state)
        state = self._add_round_key(state, round_keys[0])
        
        return self._matrix_to_bytes(state)
    
    def encrypt(self, plaintext: str, key: str) -> str:
        """
        Szyfrowanie tekstu AES
        
        Args:
            plaintext: Tekst do zaszyfrowania
            key: Klucz szyfrowania
            
        Returns:
            Zaszyfrowany tekst (hex)
        """
        try:
            app_logger.info(f"AES encryption started for text of length {len(plaintext)}")
            
            # Generowanie klucza z hasła
            key_bytes = hashlib.sha256(key.encode()).digest()[:self.key_size // 8]
            
            # Padding danych
            data = plaintext.encode('utf-8')
            padded_data = self._pad_data(data)
            
            # Rozszerzanie klucza
            round_keys = self._key_expansion(key_bytes)
            
            # Szyfrowanie bloków
            encrypted_blocks = []
            for i in range(0, len(padded_data), 16):
                block = padded_data[i:i+16]
                encrypted_block = self._encrypt_block(block, round_keys)
                encrypted_blocks.append(encrypted_block)
            
            # Konwersja na hex
            encrypted_hex = ''.join(block.hex() for block in encrypted_blocks)
            
            app_logger.info(f"AES encryption completed successfully")
            return encrypted_hex
            
        except Exception as e:
            app_logger.error(f"AES encryption failed: {str(e)}")
            raise
    
    def decrypt(self, ciphertext: str, key: str) -> str:
        """
        Deszyfrowanie tekstu AES
        
        Args:
            ciphertext: Zaszyfrowany tekst (hex)
            key: Klucz deszyfrowania
            
        Returns:
            Odszyfrowany tekst
        """
        try:
            app_logger.info(f"AES decryption started for ciphertext of length {len(ciphertext)}")
            
            # Generowanie klucza z hasła
            key_bytes = hashlib.sha256(key.encode()).digest()[:self.key_size // 8]
            
            # Konwersja hex na bajty
            cipher_bytes = bytes.fromhex(ciphertext)
            
            # Rozszerzanie klucza
            round_keys = self._key_expansion(key_bytes)
            
            # Deszyfrowanie bloków
            decrypted_blocks = []
            for i in range(0, len(cipher_bytes), 16):
                block = cipher_bytes[i:i+16]
                decrypted_block = self._decrypt_block(block, round_keys)
                decrypted_blocks.append(decrypted_block)
            
            # Łączenie bloków i usuwanie paddingu
            decrypted_data = b''.join(decrypted_blocks)
            unpadded_data = self._unpad_data(decrypted_data)
            
            app_logger.info(f"AES decryption completed successfully")
            return unpadded_data.decode('utf-8')
            
        except Exception as e:
            app_logger.error(f"AES decryption failed: {str(e)}")
            raise
    
    def encrypt_file(self, input_file: str, output_file: str, key: str) -> bool:
        """
        Szyfrowanie pliku AES
        
        Args:
            input_file: Ścieżka do pliku wejściowego
            output_file: Ścieżka do pliku wyjściowego
            key: Klucz szyfrowania
            
        Returns:
            True jeśli sukces, False w przeciwnym razie
        """
        try:
            app_logger.info(f"AES file encryption started: {input_file} -> {output_file}")
            
            # Generowanie klucza z hasła
            key_bytes = hashlib.sha256(key.encode()).digest()[:self.key_size // 8]
            
            # Rozszerzanie klucza
            round_keys = self._key_expansion(key_bytes)
            
            with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
                while True:
                    chunk = f_in.read(16)
                    if not chunk:
                        break
                    
                    # Padding ostatniego bloku
                    if len(chunk) < 16:
                        padding_length = 16 - len(chunk)
                        chunk += bytes([padding_length] * padding_length)
                    
                    # Szyfrowanie bloku
                    encrypted_chunk = self._encrypt_block(chunk, round_keys)
                    f_out.write(encrypted_chunk)
            
            app_logger.info(f"AES file encryption completed successfully")
            return True
            
        except Exception as e:
            app_logger.error(f"AES file encryption failed: {str(e)}")
            return False
    
    def decrypt_file(self, input_file: str, output_file: str, key: str) -> bool:
        """
        Deszyfrowanie pliku AES
        
        Args:
            input_file: Ścieżka do pliku wejściowego
            output_file: Ścieżka do pliku wyjściowego
            key: Klucz deszyfrowania
            
        Returns:
            True jeśli sukces, False w przeciwnym razie
        """
        try:
            app_logger.info(f"AES file decryption started: {input_file} -> {output_file}")
            
            # Generowanie klucza z hasła
            key_bytes = hashlib.sha256(key.encode()).digest()[:self.key_size // 8]
            
            # Rozszerzanie klucza
            round_keys = self._key_expansion(key_bytes)
            
            # Wczytaj cały plik do pamięci
            with open(input_file, 'rb') as f_in:
                encrypted_data = f_in.read()
            
            # Sprawdź czy plik ma odpowiedni rozmiar (wielokrotność 16)
            if len(encrypted_data) % 16 != 0:
                app_logger.error("AES file decryption failed: Invalid file size (not multiple of 16)")
                return False
            
            # Deszyfruj wszystkie bloki
            decrypted_data = bytearray()
            for i in range(0, len(encrypted_data), 16):
                block = encrypted_data[i:i+16]
                decrypted_block = self._decrypt_block(block, round_keys)
                decrypted_data.extend(decrypted_block)
            
            # Usuń padding z ostatniego bloku
            if len(decrypted_data) > 0:
                padding_length = decrypted_data[-1]
                if 1 <= padding_length <= 16:
                    # Sprawdź czy to prawidłowy padding
                    is_valid_padding = all(
                        decrypted_data[-i] == padding_length 
                        for i in range(1, padding_length + 1)
                    )
                    if is_valid_padding:
                        decrypted_data = decrypted_data[:-padding_length]
                    else:
                        app_logger.warning("AES file decryption: Invalid padding detected, keeping original data")
            
            # Zapisz odszyfrowane dane
            with open(output_file, 'wb') as f_out:
                f_out.write(decrypted_data)
            
            app_logger.info(f"AES file decryption completed successfully")
            return True
            
        except Exception as e:
            app_logger.error(f"AES file decryption failed: {str(e)}")
            return False


# Funkcje pomocnicze dla interfejsu
def aes_encrypt_text(text: str, key: str, key_size: int = 128) -> str:
    """
    Szyfrowanie tekstu AES
    
    Args:
        text: Tekst do zaszyfrowania
        key: Klucz szyfrowania
        key_size: Rozmiar klucza (128, 192, 256)
        
    Returns:
        Zaszyfrowany tekst (hex)
    """
    aes = AES(key_size)
    return aes.encrypt(text, key)


def aes_decrypt_text(ciphertext: str, key: str, key_size: int = 128) -> str:
    """
    Deszyfrowanie tekstu AES
    
    Args:
        ciphertext: Zaszyfrowany tekst (hex)
        key: Klucz deszyfrowania
        key_size: Rozmiar klucza (128, 192, 256)
        
    Returns:
        Odszyfrowany tekst
    """
    aes = AES(key_size)
    return aes.decrypt(ciphertext, key)


def aes_encrypt_file(input_file: str, output_file: str, key: str, key_size: int = 128) -> bool:
    """
    Szyfrowanie pliku AES
    
    Args:
        input_file: Ścieżka do pliku wejściowego
        output_file: Ścieżka do pliku wyjściowego
        key: Klucz szyfrowania
        key_size: Rozmiar klucza (128, 192, 256)
        
    Returns:
        True jeśli sukces, False w przeciwnym razie
    """
    aes = AES(key_size)
    return aes.encrypt_file(input_file, output_file, key)


def aes_decrypt_file(input_file: str, output_file: str, key: str, key_size: int = 128) -> bool:
    """
    Deszyfrowanie pliku AES
    
    Args:
        input_file: Ścieżka do pliku wejściowego
        output_file: Ścieżka do pliku wyjściowego
        key: Klucz deszyfrowania
        key_size: Rozmiar klucza (128, 192, 256)
        
    Returns:
        True jeśli sukces, False w przeciwnym razie
    """
    aes = AES(key_size)
    return aes.decrypt_file(input_file, output_file, key)
