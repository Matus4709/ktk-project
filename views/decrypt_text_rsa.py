"""
Okno deszyfrowania tekstu RSA
"""

import sys
import ast
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                             QWidget, QLabel, QTextEdit, QLineEdit, QPushButton, 
                             QComboBox, QMessageBox, QFrame, QGroupBox, QFileDialog)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont
from utils.rsa_cipher import rsa_decrypt_text, rsa_load_private_key
from utils.logger import AppLogger

app_logger = AppLogger()


class RSADecryptWorker(QThread):
    """Wątek do deszyfrowania RSA"""
    finished = pyqtSignal(str)
    error = pyqtSignal(str)
    
    def __init__(self, ciphertext, private_key, key_size):
        super().__init__()
        self.ciphertext = ciphertext
        self.private_key = private_key
        self.key_size = key_size
    
    def run(self):
        try:
            result = rsa_decrypt_text(self.ciphertext, self.private_key, self.key_size)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))


class RSADecryptTextWindow(QMainWindow):
    """Okno deszyfrowania tekstu RSA"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.worker = None
        self.private_key = None
        self.init_ui()
        
    def init_ui(self):
        """Inicjalizacja interfejsu użytkownika"""
        self.setWindowTitle("🔓 Deszyfrowanie tekstu - RSA")
        self.setGeometry(100, 100, 900, 700)
        self.setMinimumSize(700, 600)
        self.showMaximized()
        
        # Główny widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Główny layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # Tytuł
        title_label = QLabel("🔓 Deszyfrowanie tekstu - RSA")
        title_label.setAlignment(Qt.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                margin-bottom: 20px;
                padding: 15px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #e74c3c, stop:1 #c0392b);
                border-radius: 10px;
                color: white;
            }
        """)
        main_layout.addWidget(title_label)
        
        # Opis
        desc_label = QLabel("Wprowadź zaszyfrowany tekst i klucz prywatny do deszyfrowania.")
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("color: #7f8c8d; margin-bottom: 20px; font-size: 12px;")
        main_layout.addWidget(desc_label)
        
        # Sekcja klucza prywatnego
        key_frame = QGroupBox("🔒 Klucz prywatny RSA")
        key_frame.setFont(QFont("Arial", 12, QFont.Bold))
        key_frame.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #f44336;
                border-radius: 10px;
                margin-top: 10px;
                padding-top: 15px;
                background: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #f44336;
            }
        """)
        key_layout = QVBoxLayout(key_frame)
        
        key_label = QLabel("🔑 Wprowadź klucz prywatny (n, d) w formacie: (n, d)")
        key_label.setStyleSheet("font-weight: bold; color: #2c3e50; margin-bottom: 10px;")
        key_layout.addWidget(key_label)
        
        self.private_key_input = QTextEdit()
        self.private_key_input.setPlaceholderText("Wprowadź klucz prywatny w formacie (n, d), np: (123456789, 987654321)")
        self.private_key_input.setStyleSheet("""
            QTextEdit {
                border: 2px solid #dee2e6;
                border-radius: 8px;
                padding: 10px;
                font-size: 12px;
                background-color: white;
                font-family: 'Courier New', monospace;
            }
            QTextEdit:focus {
                border-color: #f44336;
            }
        """)
        self.private_key_input.setMaximumHeight(80)
        key_layout.addWidget(self.private_key_input)
        
        load_key_layout = QHBoxLayout()
        
        self.load_key_btn = QPushButton("🔑 Załaduj z pola")
        self.load_key_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f44336, stop:1 #d32f2f);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
                min-width: 150px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #d32f2f, stop:1 #b71c1c);
            }
        """)
        self.load_key_btn.clicked.connect(self.load_private_key)
        load_key_layout.addWidget(self.load_key_btn)
        
        self.load_from_file_btn = QPushButton("📂 Załaduj z pliku")
        self.load_from_file_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #17a2b8, stop:1 #138496);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
                min-width: 150px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #138496, stop:1 #0f6674);
            }
        """)
        self.load_from_file_btn.clicked.connect(self.load_private_key_from_file)
        load_key_layout.addWidget(self.load_from_file_btn)
        
        key_layout.addLayout(load_key_layout)
        
        main_layout.addWidget(key_frame)
        
        # Sekcja deszyfrowania
        decrypt_frame = QGroupBox("🔓 Deszyfrowanie tekstu")
        decrypt_frame.setFont(QFont("Arial", 12, QFont.Bold))
        decrypt_frame.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #3498db;
                border-radius: 10px;
                margin-top: 10px;
                padding-top: 15px;
                background: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #3498db;
            }
        """)
        decrypt_layout = QVBoxLayout(decrypt_frame)
        
        ciphertext_label = QLabel("🔒 Zaszyfrowany tekst (hex):")
        ciphertext_label.setStyleSheet("font-weight: bold; color: #2c3e50; margin-bottom: 10px;")
        decrypt_layout.addWidget(ciphertext_label)
        
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
                border-color: #3498db;
            }
        """)
        self.ciphertext_input.setMinimumHeight(120)
        decrypt_layout.addWidget(self.ciphertext_input)
        
        main_layout.addWidget(decrypt_frame)
        
        # Przyciski
        button_layout = QHBoxLayout()
        
        self.decrypt_button = QPushButton("🔓 Deszyfruj")
        self.decrypt_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e74c3c, stop:1 #c0392b);
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
                    stop:0 #c0392b, stop:1 #a93226);
            }
            QPushButton:disabled {
                background: #6c757d;
                color: #adb5bd;
            }
        """)
        self.decrypt_button.clicked.connect(self.decrypt_text)
        self.decrypt_button.setEnabled(False)
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
        """)
        self.clear_button.clicked.connect(self.clear_all)
        button_layout.addWidget(self.clear_button)
        
        self.back_button = QPushButton("⬅️ Wróć")
        self.back_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #95a5a6, stop:1 #7f8c8d);
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
                    stop:0 #7f8c8d, stop:1 #6c7b7d);
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
        
        app_logger.info("RSA decrypt text window initialized")
    
    def load_private_key(self):
        """Ładuje klucz prywatny z pola tekstowego"""
        try:
            key_text = self.private_key_input.toPlainText().strip()
            if not key_text:
                QMessageBox.warning(self, "Błąd", "Wprowadź klucz prywatny!")
                return
            
            # Próbuj sparsować jako tuple
            try:
                private_key = ast.literal_eval(key_text)
                if not isinstance(private_key, tuple) or len(private_key) != 2:
                    raise ValueError("Klucz musi być tuplą (n, d)")
                
                n, d = private_key
                if not isinstance(n, int) or not isinstance(d, int):
                    raise ValueError("Wartości klucza muszą być liczbami całkowitymi")
                
                self.private_key = (n, d)
                self.decrypt_button.setEnabled(True)
                
                QMessageBox.information(self, "Sukces", "Klucz prywatny został załadowany pomyślnie!")
                app_logger.info("RSA private key loaded successfully")
                
            except (ValueError, SyntaxError) as e:
                QMessageBox.warning(self, "Błąd", f"Nieprawidłowy format klucza!\n\nKlucz musi być w formacie: (n, d)\nPrzykład: (123456789, 987654321)\n\nBłąd: {str(e)}")
                
        except Exception as e:
            app_logger.error(f"Load private key error: {str(e)}")
            QMessageBox.critical(self, "Błąd", f"Wystąpił błąd podczas ładowania klucza:\n{str(e)}")
    
    def load_private_key_from_file(self):
        """Ładuje klucz prywatny z pliku JSON"""
        try:
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Wybierz plik z kluczem prywatnym RSA",
                "",
                "Pliki JSON (*.json);;Wszystkie pliki (*.*)"
            )
            
            if file_path:
                private_key = rsa_load_private_key(file_path)
                if private_key:
                    self.private_key = private_key
                    self.private_key_input.setPlainText(f"({private_key[0]}, {private_key[1]})")
                    self.decrypt_button.setEnabled(True)
                    QMessageBox.information(self, "Sukces", f"Klucz prywatny został załadowany z:\n{file_path}")
                    app_logger.info(f"RSA private key loaded from {file_path}")
                else:
                    QMessageBox.critical(self, "Błąd", "Nie udało się załadować klucza prywatnego!\n\nSprawdź czy plik jest poprawnym plikiem JSON z kluczem RSA.")
                    
        except Exception as e:
            app_logger.error(f"Load private key from file error: {str(e)}")
            QMessageBox.critical(self, "Błąd", f"Wystąpił błąd podczas ładowania klucza:\n{str(e)}")
    
    def decrypt_text(self):
        """Deszyfruje tekst"""
        try:
            if not self.private_key:
                QMessageBox.warning(self, "Błąd", "Najpierw załaduj klucz prywatny!")
                return
            
            ciphertext = self.ciphertext_input.toPlainText().strip()
            if not ciphertext:
                QMessageBox.warning(self, "Błąd", "Wprowadź zaszyfrowany tekst!")
                return
            
            # Wyłączenie przycisku podczas deszyfrowania
            self.decrypt_button.setEnabled(False)
            self.decrypt_button.setText("⏳ Deszyfrowanie...")
            
            # Uruchomienie wątku deszyfrowania
            key_size = self.private_key[0].bit_length()
            self.worker = RSADecryptWorker(ciphertext, self.private_key, key_size)
            self.worker.finished.connect(self.on_decryption_finished)
            self.worker.error.connect(self.on_decryption_error)
            self.worker.start()
            
            app_logger.info(f"RSA text decryption started")
            
        except Exception as e:
            app_logger.error(f"RSA text decryption error: {str(e)}")
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
            
            app_logger.info("RSA text decryption completed successfully")
            QMessageBox.information(self, "Sukces", "Tekst został odszyfrowany pomyślnie!")
            
            # Pokaż okno logów
            from views.log_window_helper import show_log_window
            show_log_window(self)
            
        except Exception as e:
            app_logger.error(f"RSA decryption finish error: {str(e)}")
            QMessageBox.critical(self, "Błąd", f"Wystąpił błąd:\n{str(e)}")
            self.decrypt_button.setEnabled(True)
            self.decrypt_button.setText("🔓 Deszyfruj")
            
            # Pokaż okno logów
            from views.log_window_helper import show_log_window
            show_log_window(self)
    
    def on_decryption_error(self, error_msg):
        """Obsługuje błąd deszyfrowania"""
        app_logger.error(f"RSA decryption error: {error_msg}")
        QMessageBox.critical(self, "Błąd deszyfrowania", f"Wystąpił błąd podczas deszyfrowania:\n{error_msg}")
        self.decrypt_button.setEnabled(True)
        self.decrypt_button.setText("🔓 Deszyfruj")
        
        # Pokaż okno logów
        from views.log_window_helper import show_log_window
        show_log_window(self)
    
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
            self.private_key_input.clear()
            self.ciphertext_input.clear()
            self.result_output.clear()
            self.private_key = None
            self.decrypt_button.setEnabled(False)
            self.copy_button.setEnabled(False)
            app_logger.info("RSA decrypt text window cleared")
        except Exception as e:
            app_logger.error(f"Clear all error: {str(e)}")
    
    def go_back(self):
        """Powraca do poprzedniego okna"""
        try:
            if self.parent:
                self.parent.show()
            self.close()
            app_logger.info("Returned to cipher choice window")
        except Exception as e:
            app_logger.error(f"Go back error: {str(e)}")
            QMessageBox.critical(self, "Błąd", f"Wystąpił błąd:\n{str(e)}")


def main():
    """Funkcja główna dla testowania"""
    app = QApplication(sys.argv)
    window = RSADecryptTextWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

