"""
Moduł do logowania działań aplikacji
"""
import logging
import sys
from datetime import datetime

class AppLogger:
    """Klasa do zarządzania logami aplikacji"""
    
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
