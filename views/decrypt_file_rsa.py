"""
Okno deszyfrowania plików RSA
"""

import sys
import os
import ast
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                             QWidget, QLabel, QLineEdit, QPushButton, QFileDialog,
                             QMessageBox, QFrame, QGroupBox, QProgressBar, QTextEdit)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont
from utils.rsa_cipher import rsa_decrypt_file, rsa_load_private_key
from utils.logger import AppLogger

app_logger = AppLogger()


class RSAFileDecryptWorker(QThread):
    """Wątek do deszyfrowania plików RSA"""
    finished = pyqtSignal(bool)
    error = pyqtSignal(str)
    progress = pyqtSignal(int)
    
    def __init__(self, input_file, output_file, private_key, key_size):
        super().__init__()
        self.input_file = input_file
        self.output_file = output_file
        self.private_key = private_key
        self.key_size = key_size
    
    def run(self):
        try:
            self.progress.emit(10)
            result = rsa_decrypt_file(self.input_file, self.output_file, self.private_key, self.key_size)
            self.progress.emit(100)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))


class RSADecryptFileWindow(QMainWindow):
    """Okno deszyfrowania plików RSA"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.worker = None
        self.private_key = None
        self.init_ui()
        
    def init_ui(self):
        """Inicjalizacja interfejsu użytkownika"""
        self.setWindowTitle("🔓 Deszyfrowanie pliku - RSA")
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
        title_label = QLabel("🔓 Deszyfrowanie pliku - RSA")
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
        desc_label = QLabel("Wprowadź zaszyfrowany plik i klucz prywatny do deszyfrowania.")
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
        
        # Sekcja plików
        file_frame = QGroupBox("📁 Pliki")
        file_frame.setFont(QFont("Arial", 12, QFont.Bold))
        file_frame.setStyleSheet("""
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
        file_layout = QVBoxLayout(file_frame)
        
        input_label = QLabel("🔒 Zaszyfrowany plik:")
        input_label.setStyleSheet("font-weight: bold; color: #2c3e50; margin-bottom: 10px;")
        file_layout.addWidget(input_label)
        
        file_input_layout = QHBoxLayout()
        self.input_file_path = QLineEdit()
        self.input_file_path.setPlaceholderText("Wybierz zaszyfrowany plik...")
        self.input_file_path.setReadOnly(True)
        self.input_file_path.setStyleSheet("""
            QLineEdit {
                border: 2px solid #dee2e6;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                background-color: white;
            }
        """)
        file_input_layout.addWidget(self.input_file_path)
        
        self.browse_input_button = QPushButton("📂 Przeglądaj")
        self.browse_input_button.setStyleSheet("""
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
        """)
        self.browse_input_button.clicked.connect(self.browse_input_file)
        file_input_layout.addWidget(self.browse_input_button)
        file_layout.addLayout(file_input_layout)
        
        output_label = QLabel("💾 Lokalizacja zapisu:")
        output_label.setStyleSheet("font-weight: bold; color: #2c3e50; margin-bottom: 10px; margin-top: 10px;")
        file_layout.addWidget(output_label)
        
        file_output_layout = QHBoxLayout()
        self.output_file_path = QLineEdit()
        self.output_file_path.setPlaceholderText("Wybierz lokalizację zapisu odszyfrowanego pliku...")
        self.output_file_path.setReadOnly(True)
        self.output_file_path.setStyleSheet("""
            QLineEdit {
                border: 2px solid #dee2e6;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                background-color: white;
            }
        """)
        file_output_layout.addWidget(self.output_file_path)
        
        self.browse_output_button = QPushButton("📂 Przeglądaj")
        self.browse_output_button.setStyleSheet("""
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
        """)
        self.browse_output_button.clicked.connect(self.browse_output_file)
        file_output_layout.addWidget(self.browse_output_button)
        file_layout.addLayout(file_output_layout)
        
        main_layout.addWidget(file_frame)
        
        # Pasek postępu
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #dee2e6;
                border-radius: 8px;
                text-align: center;
                background-color: #f8f9fa;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e74c3c, stop:1 #c0392b);
                border-radius: 6px;
            }
        """)
        main_layout.addWidget(self.progress_bar)
        
        # Przyciski
        button_layout = QHBoxLayout()
        
        self.decrypt_button = QPushButton("🔓 Deszyfruj plik")
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
                min-width: 140px;
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
        self.decrypt_button.clicked.connect(self.decrypt_file)
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
        
        # Ustawienie stylu głównego okna
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f8f9fa, stop:1 #e9ecef);
            }
        """)
        
        app_logger.info("RSA decrypt file window initialized")
    
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
    
    def browse_input_file(self):
        """Otwiera dialog wyboru pliku wejściowego"""
        try:
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Wybierz zaszyfrowany plik",
                "",
                "Pliki RSA (*.rsa);;Wszystkie pliki (*.*)"
            )
            if file_path:
                self.input_file_path.setText(file_path)
                # Automatyczne ustawienie ścieżki wyjściowej
                base_name = os.path.splitext(file_path)[0]
                if base_name.endswith("_encrypted"):
                    base_name = base_name[:-10]
                self.output_file_path.setText(f"{base_name}_decrypted")
                app_logger.info(f"Input file selected: {file_path}")
        except Exception as e:
            app_logger.error(f"Browse input file error: {str(e)}")
            QMessageBox.critical(self, "Błąd", f"Wystąpił błąd podczas wyboru pliku:\n{str(e)}")
    
    def browse_output_file(self):
        """Otwiera dialog wyboru pliku wyjściowego"""
        try:
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Wybierz lokalizację zapisu odszyfrowanego pliku",
                "",
                "Wszystkie pliki (*.*)"
            )
            if file_path:
                self.output_file_path.setText(file_path)
                app_logger.info(f"Output file selected: {file_path}")
        except Exception as e:
            app_logger.error(f"Browse output file error: {str(e)}")
            QMessageBox.critical(self, "Błąd", f"Wystąpił błąd podczas wyboru lokalizacji:\n{str(e)}")
    
    def decrypt_file(self):
        """Deszyfruje plik"""
        try:
            if not self.private_key:
                QMessageBox.warning(self, "Błąd", "Najpierw załaduj klucz prywatny!")
                return
            
            input_file = self.input_file_path.text().strip()
            output_file = self.output_file_path.text().strip()
            
            if not input_file:
                QMessageBox.warning(self, "Błąd", "Wybierz zaszyfrowany plik!")
                return
            
            if not output_file:
                QMessageBox.warning(self, "Błąd", "Wybierz lokalizację zapisu!")
                return
            
            if not os.path.exists(input_file):
                QMessageBox.warning(self, "Błąd", "Plik wejściowy nie istnieje!")
                return
            
            # Sprawdzenie czy plik wyjściowy już istnieje
            if os.path.exists(output_file):
                reply = QMessageBox.question(
                    self, 
                    "Potwierdzenie", 
                    f"Plik {os.path.basename(output_file)} już istnieje. Czy chcesz go zastąpić?",
                    QMessageBox.Yes | QMessageBox.No
                )
                if reply == QMessageBox.No:
                    return
            
            # Wyłączenie przycisku podczas deszyfrowania
            self.decrypt_button.setEnabled(False)
            self.decrypt_button.setText("⏳ Deszyfrowanie...")
            self.progress_bar.setVisible(True)
            self.progress_bar.setValue(0)
            
            # Uruchomienie wątku deszyfrowania
            key_size = self.private_key[0].bit_length()
            self.worker = RSAFileDecryptWorker(input_file, output_file, self.private_key, key_size)
            self.worker.finished.connect(self.on_decryption_finished)
            self.worker.error.connect(self.on_decryption_error)
            self.worker.progress.connect(self.progress_bar.setValue)
            self.worker.start()
            
            app_logger.info(f"RSA file decryption started: {input_file} -> {output_file}")
            
        except Exception as e:
            app_logger.error(f"RSA file decryption error: {str(e)}")
            QMessageBox.critical(self, "Błąd", f"Wystąpił błąd podczas deszyfrowania:\n{str(e)}")
            self.decrypt_button.setEnabled(True)
            self.decrypt_button.setText("🔓 Deszyfruj plik")
            self.progress_bar.setVisible(False)
    
    def on_decryption_finished(self, success):
        """Obsługuje zakończenie deszyfrowania"""
        try:
            self.decrypt_button.setEnabled(True)
            self.decrypt_button.setText("🔓 Deszyfruj plik")
            self.progress_bar.setVisible(False)
            
            if success:
                app_logger.info("RSA file decryption completed successfully")
                QMessageBox.information(
                    self, 
                    "Sukces", 
                    f"Plik został odszyfrowany pomyślnie!\n\n"
                    f"Odszyfrowany plik: {self.output_file_path.text()}"
                )
            else:
                app_logger.error("RSA file decryption failed")
                QMessageBox.critical(self, "Błąd", "Deszyfrowanie pliku nie powiodło się!")
            
        except Exception as e:
            app_logger.error(f"RSA decryption finish error: {str(e)}")
            QMessageBox.critical(self, "Błąd", f"Wystąpił błąd:\n{str(e)}")
            self.decrypt_button.setEnabled(True)
            self.decrypt_button.setText("🔓 Deszyfruj plik")
            self.progress_bar.setVisible(False)
    
    def on_decryption_error(self, error_msg):
        """Obsługuje błąd deszyfrowania"""
        app_logger.error(f"RSA file decryption error: {error_msg}")
        QMessageBox.critical(self, "Błąd deszyfrowania", f"Wystąpił błąd podczas deszyfrowania:\n{error_msg}")
        self.decrypt_button.setEnabled(True)
        self.decrypt_button.setText("🔓 Deszyfruj plik")
        self.progress_bar.setVisible(False)
    
    def clear_all(self):
        """Czyści wszystkie pola"""
        try:
            self.input_file_path.clear()
            self.output_file_path.clear()
            self.private_key_input.clear()
            self.private_key = None
            self.decrypt_button.setEnabled(False)
            self.progress_bar.setVisible(False)
            app_logger.info("RSA decrypt file window cleared")
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
    window = RSADecryptFileWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

