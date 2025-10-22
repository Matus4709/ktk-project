"""
Okno deszyfrowania tekstu AES
"""

import sys
import traceback
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                             QWidget, QLabel, QTextEdit, QLineEdit, QPushButton, 
                             QComboBox, QMessageBox, QFrame)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QIcon, QPalette, QColor, QLinearGradient, QBrush
from utils.aes_cipher import aes_decrypt_text
from utils.logger import AppLogger

app_logger = AppLogger()

class AESDecryptWorker(QThread):
    """Wątek do deszyfrowania AES"""
    finished = pyqtSignal(str)
    error = pyqtSignal(str)
    
    def __init__(self, ciphertext, key, key_size):
        super().__init__()
        self.ciphertext = ciphertext
        self.key = key
        self.key_size = key_size
    
    def run(self):
        try:
            result = aes_decrypt_text(self.ciphertext, self.key, self.key_size)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))

class AESDecryptTextWindow(QMainWindow):
    """Okno deszyfrowania tekstu AES"""
    
    def __init__(self):
        super().__init__()
        self.worker = None
        self.init_ui()
        
    def init_ui(self):
        """Inicjalizacja interfejsu użytkownika"""
        self.setWindowTitle("🔓 Deszyfrowanie tekstu - AES")
        self.setGeometry(100, 100, 800, 600)
        self.setMinimumSize(600, 500)
        
        # Główny widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Główny layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # Tytuł
        title_label = QLabel("🔓 Deszyfrowanie tekstu - AES")
        title_label.setAlignment(Qt.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #2c3e50; margin-bottom: 20px;")
        main_layout.addWidget(title_label)
        
        # Opis
        desc_label = QLabel("Wprowadź zaszyfrowany tekst (hex) i klucz. Wybierz rozmiar klucza AES.")
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setStyleSheet("color: #7f8c8d; margin-bottom: 20px;")
        main_layout.addWidget(desc_label)
        
        # Sekcja tekstu wejściowego
        input_frame = QFrame()
        input_frame.setFrameStyle(QFrame.StyledPanel)
        input_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border: 2px solid #e9ecef;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        input_layout = QVBoxLayout(input_frame)
        
        input_label = QLabel("🔒 Zaszyfrowany tekst (hex):")
        input_label.setStyleSheet("font-weight: bold; color: #2c3e50; margin-bottom: 10px;")
        input_layout.addWidget(input_label)
        
        self.ciphertext_input = QTextEdit()
        self.ciphertext_input.setPlaceholderText("Wprowadź zaszyfrowany tekst w formacie hex...")
        self.ciphertext_input.setStyleSheet("""
            QTextEdit {
                border: 2px solid #dee2e6;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                background-color: white;
                font-family: 'Courier New', monospace;
            }
            QTextEdit:focus {
                border-color: #007bff;
            }
        """)
        self.ciphertext_input.setMinimumHeight(120)
        input_layout.addWidget(self.ciphertext_input)
        
        main_layout.addWidget(input_frame)
        
        # Sekcja klucza
        key_frame = QFrame()
        key_frame.setFrameStyle(QFrame.StyledPanel)
        key_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border: 2px solid #e9ecef;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        key_layout = QVBoxLayout(key_frame)
        
        key_label = QLabel("🔑 Klucz deszyfrowania:")
        key_label.setStyleSheet("font-weight: bold; color: #2c3e50; margin-bottom: 10px;")
        key_layout.addWidget(key_label)
        
        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("Wprowadź klucz deszyfrowania...")
        self.key_input.setEchoMode(QLineEdit.Password)
        self.key_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #dee2e6;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #007bff;
            }
        """)
        key_layout.addWidget(self.key_input)
        
        # Rozmiar klucza
        key_size_layout = QHBoxLayout()
        key_size_label = QLabel("🔧 Rozmiar klucza:")
        key_size_label.setStyleSheet("font-weight: bold; color: #2c3e50;")
        key_size_layout.addWidget(key_size_label)
        
        self.key_size_combo = QComboBox()
        self.key_size_combo.addItems(["128 bitów (AES-128)", "192 bity (AES-192)", "256 bitów (AES-256)"])
        self.key_size_combo.setCurrentIndex(0)  # Domyślnie AES-128
        self.key_size_combo.setStyleSheet("""
            QComboBox {
                border: 2px solid #dee2e6;
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
                background-color: white;
                min-width: 200px;
            }
            QComboBox:focus {
                border-color: #007bff;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #6c757d;
                margin-right: 10px;
            }
        """)
        key_size_layout.addWidget(self.key_size_combo)
        key_size_layout.addStretch()
        
        key_layout.addLayout(key_size_layout)
        main_layout.addWidget(key_frame)
        
        # Przyciski
        button_layout = QHBoxLayout()
        
        self.decrypt_button = QPushButton("🔓 Deszyfruj")
        self.decrypt_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #dc3545, stop:1 #c82333);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 16px;
                font-weight: bold;
                min-width: 120px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #c82333, stop:1 #bd2130);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #bd2130, stop:1 #a71e2a);
            }
            QPushButton:disabled {
                background: #6c757d;
                color: #adb5bd;
            }
        """)
        self.decrypt_button.clicked.connect(self.decrypt_text)
        button_layout.addWidget(self.decrypt_button)
        
        self.clear_button = QPushButton("🗑️ Wyczyść")
        self.clear_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #6c757d, stop:1 #495057);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 16px;
                font-weight: bold;
                min-width: 120px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #495057, stop:1 #343a40);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #343a40, stop:1 #212529);
            }
        """)
        self.clear_button.clicked.connect(self.clear_all)
        button_layout.addWidget(self.clear_button)
        
        self.back_button = QPushButton("⬅️ Wróć")
        self.back_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #28a745, stop:1 #1e7e34);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 16px;
                font-weight: bold;
                min-width: 120px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1e7e34, stop:1 #155724);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #155724, stop:1 #0c4a1a);
            }
        """)
        self.back_button.clicked.connect(self.go_back)
        button_layout.addWidget(self.back_button)
        
        button_layout.addStretch()
        main_layout.addLayout(button_layout)
        
        # Sekcja wyniku
        result_frame = QFrame()
        result_frame.setFrameStyle(QFrame.StyledPanel)
        result_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border: 2px solid #e9ecef;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        result_layout = QVBoxLayout(result_frame)
        
        result_label = QLabel("📝 Odszyfrowany tekst:")
        result_label.setStyleSheet("font-weight: bold; color: #2c3e50; margin-bottom: 10px;")
        result_layout.addWidget(result_label)
        
        self.result_output = QTextEdit()
        self.result_output.setPlaceholderText("Odszyfrowany tekst pojawi się tutaj...")
        self.result_output.setReadOnly(True)
        self.result_output.setStyleSheet("""
            QTextEdit {
                border: 2px solid #dee2e6;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                background-color: white;
            }
        """)
        self.result_output.setMinimumHeight(120)
        result_layout.addWidget(self.result_output)
        
        # Przycisk kopiowania
        copy_layout = QHBoxLayout()
        copy_layout.addStretch()
        
        self.copy_button = QPushButton("📋 Kopiuj wynik")
        self.copy_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #17a2b8, stop:1 #138496);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #138496, stop:1 #0f6674);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0f6674, stop:1 #0b4d56);
            }
            QPushButton:disabled {
                background: #6c757d;
                color: #adb5bd;
            }
        """)
        self.copy_button.clicked.connect(self.copy_result)
        self.copy_button.setEnabled(False)
        copy_layout.addWidget(self.copy_button)
        
        result_layout.addLayout(copy_layout)
        main_layout.addWidget(result_frame)
        
        # Ustawienie stylu głównego okna
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f8f9fa, stop:1 #e9ecef);
            }
        """)
        
        app_logger.info("AES decrypt text window initialized")
    
    def get_key_size(self):
        """Pobiera rozmiar klucza z combobox"""
        selection = self.key_size_combo.currentText()
        if "128" in selection:
            return 128
        elif "192" in selection:
            return 192
        elif "256" in selection:
            return 256
        return 128
    
    def decrypt_text(self):
        """Deszyfruje tekst"""
        try:
            ciphertext = self.ciphertext_input.toPlainText().strip()
            key = self.key_input.text().strip()
            
            if not ciphertext:
                QMessageBox.warning(self, "Błąd", "Wprowadź zaszyfrowany tekst!")
                return
            
            if not key:
                QMessageBox.warning(self, "Błąd", "Wprowadź klucz deszyfrowania!")
                return
            
            # Sprawdzenie czy tekst jest w formacie hex
            try:
                bytes.fromhex(ciphertext)
            except ValueError:
                QMessageBox.warning(self, "Błąd", "Zaszyfrowany tekst musi być w formacie hex!")
                return
            
            # Wyłączenie przycisku podczas deszyfrowania
            self.decrypt_button.setEnabled(False)
            self.decrypt_button.setText("⏳ Deszyfrowanie...")
            
            # Uruchomienie wątku deszyfrowania
            self.worker = AESDecryptWorker(ciphertext, key, self.get_key_size())
            self.worker.finished.connect(self.on_decryption_finished)
            self.worker.error.connect(self.on_decryption_error)
            self.worker.start()
            
            app_logger.info(f"AES text decryption started with key size {self.get_key_size()}")
            
        except Exception as e:
            app_logger.error(f"AES text decryption error: {str(e)}")
            QMessageBox.critical(self, "Błąd", f"Wystąpił błąd podczas deszyfrowania:\n{str(e)}")
            self.decrypt_button.setEnabled(True)
            self.decrypt_button.setText("🔓 Deszyfruj")
    
    def on_decryption_finished(self, result):
        """Obsługuje zakończenie deszyfrowania"""
        try:
            self.result_output.setPlainText(result)
            self.copy_button.setEnabled(True)
            self.decrypt_button.setEnabled(True)
            self.decrypt_button.setText("🔓 Deszyfruj")
            
            app_logger.info("AES text decryption completed successfully")
            QMessageBox.information(self, "Sukces", "Tekst został odszyfrowany pomyślnie!")
            
        except Exception as e:
            app_logger.error(f"AES decryption finish error: {str(e)}")
            QMessageBox.critical(self, "Błąd", f"Wystąpił błąd:\n{str(e)}")
            self.decrypt_button.setEnabled(True)
            self.decrypt_button.setText("🔓 Deszyfruj")
    
    def on_decryption_error(self, error_msg):
        """Obsługuje błąd deszyfrowania"""
        app_logger.error(f"AES decryption error: {error_msg}")
        QMessageBox.critical(self, "Błąd deszyfrowania", f"Wystąpił błąd podczas deszyfrowania:\n{error_msg}")
        self.decrypt_button.setEnabled(True)
        self.decrypt_button.setText("🔓 Deszyfruj")
    
    def copy_result(self):
        """Kopiuje wynik do schowka"""
        try:
            result = self.result_output.toPlainText()
            if result:
                clipboard = QApplication.clipboard()
                clipboard.setText(result)
                QMessageBox.information(self, "Sukces", "Wynik został skopiowany do schowka!")
            else:
                QMessageBox.warning(self, "Błąd", "Brak wyniku do skopiowania!")
        except Exception as e:
            app_logger.error(f"Copy result error: {str(e)}")
            QMessageBox.critical(self, "Błąd", f"Wystąpił błąd podczas kopiowania:\n{str(e)}")
    
    def clear_all(self):
        """Czyści wszystkie pola"""
        try:
            self.ciphertext_input.clear()
            self.key_input.clear()
            self.result_output.clear()
            self.copy_button.setEnabled(False)
            app_logger.info("AES decrypt text window cleared")
        except Exception as e:
            app_logger.error(f"Clear all error: {str(e)}")
    
    def go_back(self):
        """Powraca do poprzedniego okna"""
        try:
            from views.cipher_choice_window import CipherChoiceWindow
            self.cipher_window = CipherChoiceWindow()
            self.cipher_window.show()
            self.close()
            app_logger.info("Returned to cipher choice window")
        except Exception as e:
            app_logger.error(f"Go back error: {str(e)}")
            QMessageBox.critical(self, "Błąd", f"Wystąpił błąd:\n{str(e)}")

def main():
    """Funkcja główna dla testowania"""
    app = QApplication(sys.argv)
    window = AESDecryptTextWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
