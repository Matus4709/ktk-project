"""
Okno deszyfrowania plików AES
"""

import sys
import os
import traceback
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                             QWidget, QLabel, QLineEdit, QPushButton, QFileDialog,
                             QComboBox, QMessageBox, QFrame, QProgressBar)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QIcon, QPalette, QColor, QLinearGradient, QBrush
from utils.aes_cipher import aes_decrypt_file
from utils.logger import AppLogger

app_logger = AppLogger()

class AESFileDecryptWorker(QThread):
    """Wątek do deszyfrowania plików AES"""
    finished = pyqtSignal(bool)
    error = pyqtSignal(str)
    progress = pyqtSignal(int)
    
    def __init__(self, input_file, output_file, key, key_size):
        super().__init__()
        self.input_file = input_file
        self.output_file = output_file
        self.key = key
        self.key_size = key_size
    
    def run(self):
        try:
            self.progress.emit(10)
            result = aes_decrypt_file(self.input_file, self.output_file, self.key, self.key_size)
            self.progress.emit(100)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))

class AESDecryptFileWindow(QMainWindow):
    """Okno deszyfrowania plików AES"""
    
    def __init__(self):
        super().__init__()
        self.worker = None
        self.init_ui()
        
    def init_ui(self):
        """Inicjalizacja interfejsu użytkownika"""
        self.setWindowTitle("🔓 Deszyfrowanie pliku - AES")
        self.setGeometry(100, 100, 700, 500)
        self.setMinimumSize(600, 400)
        
        # Główny widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Główny layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # Tytuł
        title_label = QLabel("🔓 Deszyfrowanie pliku - AES")
        title_label.setAlignment(Qt.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #2c3e50; margin-bottom: 20px;")
        main_layout.addWidget(title_label)
        
        # Opis
        desc_label = QLabel("Wybierz zaszyfrowany plik, podaj klucz i wybierz lokalizację zapisu.")
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setStyleSheet("color: #7f8c8d; margin-bottom: 20px;")
        main_layout.addWidget(desc_label)
        
        # Sekcja pliku wejściowego
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
        
        input_label = QLabel("🔒 Zaszyfrowany plik:")
        input_label.setStyleSheet("font-weight: bold; color: #2c3e50; margin-bottom: 10px;")
        input_layout.addWidget(input_label)
        
        file_layout = QHBoxLayout()
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
        file_layout.addWidget(self.input_file_path)
        
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
                min-width: 120px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #138496, stop:1 #0f6674);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0f6674, stop:1 #0b4d56);
            }
        """)
        self.browse_input_button.clicked.connect(self.browse_input_file)
        file_layout.addWidget(self.browse_input_button)
        
        input_layout.addLayout(file_layout)
        main_layout.addWidget(input_frame)
        
        # Sekcja pliku wyjściowego
        output_frame = QFrame()
        output_frame.setFrameStyle(QFrame.StyledPanel)
        output_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border: 2px solid #e9ecef;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        output_layout = QVBoxLayout(output_frame)
        
        output_label = QLabel("💾 Lokalizacja zapisu:")
        output_label.setStyleSheet("font-weight: bold; color: #2c3e50; margin-bottom: 10px;")
        output_layout.addWidget(output_label)
        
        output_file_layout = QHBoxLayout()
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
        output_file_layout.addWidget(self.output_file_path)
        
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
                min-width: 120px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #138496, stop:1 #0f6674);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0f6674, stop:1 #0b4d56);
            }
        """)
        self.browse_output_button.clicked.connect(self.browse_output_file)
        output_file_layout.addWidget(self.browse_output_button)
        
        output_layout.addLayout(output_file_layout)
        main_layout.addWidget(output_frame)
        
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
                    stop:0 #dc3545, stop:1 #c82333);
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
                    stop:0 #dc3545, stop:1 #c82333);
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
        self.decrypt_button.clicked.connect(self.decrypt_file)
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
        
        # Ustawienie stylu głównego okna
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f8f9fa, stop:1 #e9ecef);
            }
        """)
        
        app_logger.info("AES decrypt file window initialized")
    
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
    
    def browse_input_file(self):
        """Otwiera dialog wyboru pliku wejściowego"""
        try:
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Wybierz zaszyfrowany plik",
                "",
                "Pliki AES (*.aes);;Wszystkie pliki (*.*)"
            )
            if file_path:
                self.input_file_path.setText(file_path)
                # Automatyczne ustawienie ścieżki wyjściowej
                base_name = os.path.splitext(file_path)[0]
                if base_name.endswith("_encrypted"):
                    base_name = base_name[:-10]  # Usuń "_encrypted"
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
            input_file = self.input_file_path.text().strip()
            output_file = self.output_file_path.text().strip()
            key = self.key_input.text().strip()
            
            if not input_file:
                QMessageBox.warning(self, "Błąd", "Wybierz zaszyfrowany plik!")
                return
            
            if not output_file:
                QMessageBox.warning(self, "Błąd", "Wybierz lokalizację zapisu!")
                return
            
            if not key:
                QMessageBox.warning(self, "Błąd", "Wprowadź klucz deszyfrowania!")
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
            self.worker = AESFileDecryptWorker(input_file, output_file, key, self.get_key_size())
            self.worker.finished.connect(self.on_decryption_finished)
            self.worker.error.connect(self.on_decryption_error)
            self.worker.progress.connect(self.progress_bar.setValue)
            self.worker.start()
            
            app_logger.info(f"AES file decryption started: {input_file} -> {output_file}")
            
        except Exception as e:
            app_logger.error(f"AES file decryption error: {str(e)}")
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
                app_logger.info("AES file decryption completed successfully")
                QMessageBox.information(
                    self, 
                    "Sukces", 
                    f"Plik został odszyfrowany pomyślnie!\n\nOdszyfrowany plik: {self.output_file_path.text()}"
                )
            else:
                app_logger.error("AES file decryption failed")
                QMessageBox.critical(self, "Błąd", "Deszyfrowanie pliku nie powiodło się!")
            
        except Exception as e:
            app_logger.error(f"AES decryption finish error: {str(e)}")
            QMessageBox.critical(self, "Błąd", f"Wystąpił błąd:\n{str(e)}")
            self.decrypt_button.setEnabled(True)
            self.decrypt_button.setText("🔓 Deszyfruj plik")
            self.progress_bar.setVisible(False)
    
    def on_decryption_error(self, error_msg):
        """Obsługuje błąd deszyfrowania"""
        app_logger.error(f"AES file decryption error: {error_msg}")
        QMessageBox.critical(self, "Błąd deszyfrowania", f"Wystąpił błąd podczas deszyfrowania:\n{error_msg}")
        self.decrypt_button.setEnabled(True)
        self.decrypt_button.setText("🔓 Deszyfruj plik")
        self.progress_bar.setVisible(False)
    
    def clear_all(self):
        """Czyści wszystkie pola"""
        try:
            self.input_file_path.clear()
            self.output_file_path.clear()
            self.key_input.clear()
            self.progress_bar.setVisible(False)
            app_logger.info("AES decrypt file window cleared")
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
    window = AESDecryptFileWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
