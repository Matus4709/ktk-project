"""
Moduł do logowania działań aplikacji z szczegółowym logowaniem krok po kroku
"""
import logging
import sys
from datetime import datetime
from typing import List, Dict, Optional
from collections import deque

class AppLogger:
    """Klasa do zarządzania logami aplikacji z szczegółowym logowaniem operacji"""
    
    def __init__(self):
        self.logger = logging.getLogger('ktk_app')
        self.logger.setLevel(logging.INFO)
        
        # Usuń istniejące handlery żeby uniknąć duplikatów
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)
        
        # Handler do konsoli
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        
        # Format logów
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)s | %(message)s',
            datefmt='%H:%M:%S'
        )
        console_handler.setFormatter(formatter)
        
        self.logger.addHandler(console_handler)
        
        # Wyłącz propagację do root logger
        self.logger.propagate = False
        
        # Lista szczegółowych logów operacji (ostatnie 100 operacji)
        self.detailed_logs: deque = deque(maxlen=100)
        self.current_operation_log: List[Dict] = []
        self.current_operation_name: Optional[str] = None
    
    def info(self, message):
        """Log informacyjny"""
        self.logger.info(message)
    
    def warning(self, message):
        """Log ostrzeżenia"""
        self.logger.warning(message)
    
    def error(self, message):
        """Log błędu"""
        self.logger.error(message)
    
    def debug(self, message):
        """Log debug"""
        self.logger.debug(message)
    
    def start_operation(self, operation_name: str, algorithm: str, operation_type: str = "encrypt"):
        """
        Rozpoczyna nową operację szyfrowania/deszyfrowania
        
        Args:
            operation_name: Nazwa operacji (np. "AES Encryption")
            algorithm: Nazwa algorytmu (np. "AES", "RSA", "Caesar")
            operation_type: Typ operacji ("encrypt" lub "decrypt")
        """
        self.current_operation_log = []
        self.current_operation_name = operation_name
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Opisy algorytmów
        algorithm_descriptions = {
            "AES": "AES (Advanced Encryption Standard) to symetryczny szyfr blokowy używany na całym świecie.\n"
                   "Działa na blokach 128 bitów (16 bajtów) i używa kluczy 128, 192 lub 256 bitów.\n"
                   "Algorytm wykonuje 10-14 rund transformacji (w zależności od rozmiaru klucza).\n"
                   "Każda runda składa się z: SubBytes, ShiftRows, MixColumns i AddRoundKey.\n"
                   "AES jest bardzo bezpieczny i jest standardem używanym przez rządy i organizacje.",
            
            "RSA": "RSA (Rivest-Shamir-Adleman) to asymetryczny szyfr kryptograficzny.\n"
                   "Używa pary kluczy: klucza publicznego do szyfrowania i klucza prywatnego do deszyfrowania.\n"
                   "Bezpieczeństwo opiera się na trudności faktoryzacji dużych liczb pierwszych.\n"
                   "Szyfrowanie: c = m^e mod n, gdzie m to wiadomość, e to wykładnik publiczny, n to moduł.\n"
                   "Deszyfrowanie: m = c^d mod n, gdzie d to wykładnik prywatny.\n"
                   "RSA jest używany do szyfrowania danych, podpisów cyfrowych i wymiany kluczy.",
            
            "Caesar": "Szyfr Cezara to jeden z najstarszych i najprostszych szyfrów podstawieniowych.\n"
                     "Działa poprzez przesunięcie każdej litery alfabetu o stałą liczbę pozycji (1-25).\n"
                     "Na przykład z przesunięciem 3: A→D, B→E, C→F, ..., Z→C (zawijanie).\n"
                     "Znaki niealfabetyczne (spacje, cyfry, znaki specjalne) pozostają bez zmian.\n"
                     "Szyfr Cezara jest łatwy do złamania przez analizę częstotliwości liter.\n"
                     "Używany głównie do celów edukacyjnych i prostych zastosowań.",
            
            "Vigenere": "Szyfr Vigenère to polialfabetyczny szyfr podstawieniowy, ulepszona wersja szyfru Cezara.\n"
                       "Zamiast stałego przesunięcia, używa klucza słownego do określenia przesunięcia dla każdej litery.\n"
                       "Każda litera klucza określa przesunięcie dla odpowiadającej litery tekstu.\n"
                       "Klucz jest powtarzany cyklicznie, jeśli tekst jest dłuższy niż klucz.\n"
                       "Dzięki temu ta sama litera w tekście może być szyfrowana różnymi literami w zależności od pozycji.\n"
                       "Jest bardziej bezpieczny niż szyfr Cezara, ale nadal podatny na ataki kryptoanalityczne.",
            
            "Stream Cipher": "Szyfr strumieniowy (Stream Cipher) szyfruje dane bit po bicie lub bajt po bajcie.\n"
                           "Używa pseudolosowego strumienia klucza generowanego z ziarna (seed).\n"
                           "Każdy bajt tekstu jest szyfrowany przez operację XOR z odpowiadającym bajtem strumienia klucza.\n"
                           "Strumień klucza jest generowany deterministycznie z ziarna używając funkcji hash (SHA-256).\n"
                           "XOR ma właściwość: (A XOR B) XOR B = A, co pozwala na łatwe deszyfrowanie.\n"
                           "Szyfry strumieniowe są szybkie i efektywne, używane w komunikacji w czasie rzeczywistym."
        }
        
        self.add_step("START", f"Rozpoczęto operację: {operation_name}")
        self.add_step("INFO", f"Algorytm: {algorithm}")
        
        # Dodaj szczegółowy opis algorytmu
        description = algorithm_descriptions.get(algorithm, f"Algorytm {algorithm}")
        self.add_step("EXPLANATION", f"Opis algorytmu {algorithm}",
                      explanation=description)
        
        self.add_step("INFO", f"Typ operacji: {'Szyfrowanie' if operation_type == 'encrypt' else 'Deszyfrowanie'}")
        self.add_step("INFO", f"Czas rozpoczęcia: {timestamp}")
    
    def add_step(self, step_type: str, message: str, details: Optional[Dict] = None, explanation: Optional[str] = None):
        """
        Dodaje krok do bieżącej operacji
        
        Args:
            step_type: Typ kroku ("STEP", "INFO", "WARNING", "ERROR", "SUCCESS", "EXPLANATION")
            message: Wiadomość kroku
            details: Opcjonalne szczegóły (słownik)
            explanation: Opcjonalne szczegółowe wyjaśnienie działania
        """
        step = {
            "type": step_type,
            "message": message,
            "timestamp": datetime.now().strftime("%H:%M:%S.%f")[:-3],
            "details": details or {},
            "explanation": explanation
        }
        self.current_operation_log.append(step)
        
        # Również loguj do standardowego loggera
        if step_type == "ERROR":
            self.error(message)
        elif step_type == "WARNING":
            self.warning(message)
        else:
            self.info(message)
    
    def finish_operation(self, success: bool = True, result_summary: Optional[str] = None):
        """
        Kończy bieżącą operację i zapisuje log
        
        Args:
            success: Czy operacja zakończyła się sukcesem
            result_summary: Podsumowanie wyniku
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if success:
            self.add_step("SUCCESS", f"Operacja zakończona pomyślnie: {self.current_operation_name}")
        else:
            self.add_step("ERROR", f"Operacja zakończona z błędem: {self.current_operation_name}")
        
        if result_summary:
            self.add_step("INFO", f"Podsumowanie: {result_summary}")
        
        self.add_step("END", f"Czas zakończenia: {timestamp}")
        
        # Zapisz log operacji
        operation_log = {
            "name": self.current_operation_name,
            "timestamp": timestamp,
            "success": success,
            "steps": list(self.current_operation_log)
        }
        self.detailed_logs.append(operation_log)
        
        # Wyczyść bieżący log
        self.current_operation_log = []
        self.current_operation_name = None
    
    def get_last_operation_log(self) -> Optional[Dict]:
        """Zwraca log ostatniej operacji"""
        if self.detailed_logs:
            return self.detailed_logs[-1]
        return None
    
    def get_all_logs(self) -> List[Dict]:
        """Zwraca wszystkie zapisane logi"""
        return list(self.detailed_logs)
    
    def clear_logs(self):
        """Czyści wszystkie logi"""
        self.detailed_logs.clear()
        self.current_operation_log = []
        self.current_operation_name = None
    
    def format_log_for_display(self, log: Dict) -> str:
        """
        Formatuje log do wyświetlenia w oknie z szczegółowymi wyjaśnieniami
        
        Args:
            log: Słownik z logiem operacji
            
        Returns:
            Sformatowany tekst logu
        """
        lines = []
        lines.append("=" * 100)
        lines.append(f"OPERACJA: {log['name']}")
        lines.append(f"CZAS: {log['timestamp']}")
        lines.append(f"STATUS: {'✓ SUKCES' if log['success'] else '✗ BŁĄD'}")
        lines.append("=" * 100)
        lines.append("")
        lines.append("📖 SZCZEGÓŁOWE WYJAŚNIENIE DZIAŁANIA ALGORYTMU KROK PO KROKU")
        lines.append("")
        lines.append("-" * 100)
        lines.append("")
        
        for i, step in enumerate(log['steps'], 1):
            step_type = step['type']
            message = step['message']
            timestamp = step['timestamp']
            explanation = step.get('explanation')
            
            # Ikony dla różnych typów kroków
            icons = {
                "START": "▶",
                "STEP": "  →",
                "INFO": "  ℹ",
                "WARNING": "  ⚠",
                "ERROR": "  ✗",
                "SUCCESS": "  ✓",
                "END": "■",
                "EXPLANATION": "  📝"
            }
            icon = icons.get(step_type, "  •")
            
            # Nagłówek kroku
            lines.append(f"KROK {i}: [{timestamp}] {icon} {message}")
            lines.append("")
            
            # Dodaj szczegółowe wyjaśnienie jeśli istnieje
            if explanation:
                lines.append("    📚 WYJAŚNIENIE:")
                # Formatuj wyjaśnienie z wcięciami
                explanation_lines = explanation.split('\n')
                for exp_line in explanation_lines:
                    if exp_line.strip():
                        lines.append(f"       {exp_line}")
                lines.append("")
            
            # Dodaj szczegóły jeśli istnieją
            if step.get('details'):
                lines.append("    📊 SZCZEGÓŁY:")
                for key, value in step['details'].items():
                    # Formatuj wartości
                    if isinstance(value, str):
                        # Skróć bardzo długie wartości, ale pokaż więcej niż wcześniej
                        if len(value) > 200:
                            value = value[:200] + f"... (pokazano 200 z {len(value)} znaków)"
                        # Zachowaj formatowanie dla wieloliniowych wartości
                        if '\n' in value:
                            value_lines = value.split('\n')
                            lines.append(f"       {key}:")
                            for val_line in value_lines[:10]:  # Maksymalnie 10 linii
                                lines.append(f"          {val_line}")
                            if len(value_lines) > 10:
                                lines.append(f"          ... (i {len(value_lines) - 10} więcej linii)")
                        else:
                            lines.append(f"       {key}: {value}")
                    else:
                        lines.append(f"       {key}: {value}")
                lines.append("")
            
            lines.append("-" * 100)
            lines.append("")
        
        lines.append("=" * 100)
        return "\n".join(lines)
    
    def log_app_start(self):
        """Log uruchomienia aplikacji"""
        self.info("Aplikacja KTK uruchomiona")
        self.info("Data: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    def log_window_open(self, window_name):
        """Log otwarcia okna"""
        self.info(f"Otwarto okno: {window_name}")
    
    def log_encryption_start(self, text_type, shift):
        """Log rozpoczęcia szyfrowania"""
        self.info(f"Rozpoczęto szyfrowanie {text_type} z przesunięciem {shift}")
    
    def log_encryption_success(self, text_type, result_length):
        """Log udanego szyfrowania"""
        self.info(f"Szyfrowanie {text_type} zakończone pomyślnie (długość: {result_length} znaków)")
    
    def log_decryption_start(self, text_type, shift):
        """Log rozpoczęcia deszyfrowania"""
        self.info(f"Rozpoczęto deszyfrowanie {text_type} z przesunięciem {shift}")
    
    def log_decryption_success(self, text_type, result_length):
        """Log udanego deszyfrowania"""
        self.info(f"Deszyfrowanie {text_type} zakończone pomyślnie (długość: {result_length} znaków)")
    
    def log_file_operation(self, operation, file_path, shift):
        """Log operacji na pliku"""
        self.info(f"{operation} pliku: {file_path} (przesunięcie: {shift})")
    
    def log_file_success(self, operation, input_file, output_file):
        """Log udanej operacji na pliku"""
        self.info(f"{operation} pliku zakończone: {input_file} -> {output_file}")
    
    def log_preview(self, operation, file_path, shift):
        """Log podglądu operacji"""
        self.info(f"Podgląd {operation} pliku: {file_path} (przesunięcie: {shift})")
    
    def log_error(self, operation, error_msg):
        """Log błędu"""
        self.error(f"Błąd podczas {operation}: {error_msg}")
    
    def log_validation_error(self, field, value):
        """Log błędu walidacji"""
        self.warning(f"Błąd walidacji {field}: {value}")
    
    def log_user_action(self, action):
        """Log akcji użytkownika"""
        self.info(f"Użytkownik: {action}")

# Globalna instancja loggera
app_logger = AppLogger()
