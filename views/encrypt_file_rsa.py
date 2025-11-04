"""
Okno szyfrowania plików RSA
"""

import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                             QWidget, QLabel, QLineEdit, QPushButton, QFileDialog,
                             QComboBox, QMessageBox, QFrame, QGroupBox, QProgressBar, QTextEdit)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont
from utils.rsa_cipher import rsa_encrypt_file, rsa_generate_key_pair, rsa_save_key_pair, rsa_save_public_key, rsa_save_private_key
from utils.logger import AppLogger

app_logger = AppLogger()


class RSAFileEncryptWorker(QThread):
    """Wątek do szyfrowania plików RSA"""
    finished = pyqtSignal(bool)
    error = pyqtSignal(str)
    progress = pyqtSignal(int)
    
    def __init__(self, input_file, output_file, public_key, key_size):
        super().__init__()
        self.input_file = input_file
        self.output_file = output_file
        self.public_key = public_key
        self.key_size = key_size
    
    def run(self):
        try:
            self.progress.emit(10)
            result = rsa_encrypt_file(self.input_file, self.output_file, self.public_key, self.key_size)
            self.progress.emit(100)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))


class RSAFileKeyGenWorker(QThread):
    """Wątek do generowania kluczy RSA"""
    finished = pyqtSignal(tuple)
    error = pyqtSignal(str)
    
    def __init__(self, key_size):
        super().__init__()
        self.key_size = key_size
    
    def run(self):
        try:
            key_pair = rsa_generate_key_pair(self.key_size)
            self.finished.emit(key_pair)
        except Exception as e:
            self.error.emit(str(e))


class RSAEncryptFileWindow(QMainWindow):
    """Okno szyfrowania plików RSA"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.worker = None
        self.key_gen_worker = None
        self.public_key = None
        self.private_key = None
        self.init_ui()
        
    def init_ui(self):
        """Inicjalizacja interfejsu użytkownika"""
        self.setWindowTitle("🔑 Szyfrowanie pliku - RSA")
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
        title_label = QLabel("🔑 Szyfrowanie pliku - RSA")
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
                    stop:0 #f39c12, stop:1 #e67e22);
                border-radius: 10px;
                color: white;
            }
        """)
        main_layout.addWidget(title_label)
        
        # Opis
        desc_label = QLabel("RSA to szyfr asymetryczny. Najpierw wygeneruj parę kluczy, następnie użyj klucza publicznego do szyfrowania pliku.")
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("color: #7f8c8d; margin-bottom: 20px; font-size: 12px;")
        main_layout.addWidget(desc_label)
        
        # Sekcja generowania kluczy
        key_gen_frame = QGroupBox("🔑 Generowanie kluczy RSA")
        key_gen_frame.setFont(QFont("Arial", 12, QFont.Bold))
        key_gen_frame.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #f39c12;
                border-radius: 10px;
                margin-top: 10px;
                padding-top: 15px;
                background: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #f39c12;
            }
        """)
        key_gen_layout = QVBoxLayout(key_gen_frame)
        
        key_size_layout = QHBoxLayout()
        key_size_label = QLabel("🔧 Rozmiar klucza:")
        key_size_label.setStyleSheet("font-weight: bold; color: #2c3e50;")
        key_size_layout.addWidget(key_size_label)
        
        self.key_size_combo = QComboBox()
        self.key_size_combo.addItems(["512 bitów", "1024 bity (zalecane)", "2048 bitów"])
        self.key_size_combo.setCurrentIndex(1)  # Domyślnie 1024
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
                border-color: #f39c12;
            }
        """)
        key_size_layout.addWidget(self.key_size_combo)
        key_size_layout.addStretch()
        key_gen_layout.addLayout(key_size_layout)
        
        self.generate_key_btn = QPushButton("🔑 Generuj parę kluczy")
        self.generate_key_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f39c12, stop:1 #e67e22);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
                min-width: 200px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e67e22, stop:1 #d35400);
            }
            QPushButton:disabled {
                background: #6c757d;
                color: #adb5bd;
            }
        """)
        self.generate_key_btn.clicked.connect(self.generate_keys)
        key_gen_layout.addWidget(self.generate_key_btn)
        
        # Wyświetlanie kluczy
        key_display_layout = QHBoxLayout()
        
        # Klucz publiczny
        public_key_frame = QFrame()
        public_key_frame.setStyleSheet("""
            QFrame {
                background-color: #e8f5e9;
                border: 2px solid #4caf50;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        public_key_layout = QVBoxLayout(public_key_frame)
        public_key_label = QLabel("🔓 Klucz publiczny (n, e):")
        public_key_label.setStyleSheet("font-weight: bold; color: #2c3e50;")
        public_key_layout.addWidget(public_key_label)
        
        self.public_key_display = QTextEdit()
        self.public_key_display.setPlaceholderText("Klucz publiczny pojawi się tutaj po wygenerowaniu...")
        self.public_key_display.setReadOnly(True)
        self.public_key_display.setMaximumHeight(80)
        self.public_key_display.setStyleSheet("""
            QTextEdit {
                border: 1px solid #4caf50;
                border-radius: 5px;
                padding: 5px;
                font-size: 11px;
                background-color: white;
                font-family: 'Courier New', monospace;
            }
        """)
        public_key_layout.addWidget(self.public_key_display)
        key_display_layout.addWidget(public_key_frame)
        
        # Klucz prywatny
        private_key_frame = QFrame()
        private_key_frame.setStyleSheet("""
            QFrame {
                background-color: #ffebee;
                border: 2px solid #f44336;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        private_key_layout = QVBoxLayout(private_key_frame)
        private_key_label = QLabel("🔒 Klucz prywatny (n, d):")
        private_key_label.setStyleSheet("font-weight: bold; color: #2c3e50;")
        private_key_layout.addWidget(private_key_label)
        
        self.private_key_display = QTextEdit()
        self.private_key_display.setPlaceholderText("Klucz prywatny pojawi się tutaj po wygenerowaniu...")
        self.private_key_display.setReadOnly(True)
        self.private_key_display.setMaximumHeight(80)
        self.private_key_display.setStyleSheet("""
            QTextEdit {
                border: 1px solid #f44336;
                border-radius: 5px;
                padding: 5px;
                font-size: 11px;
                background-color: white;
                font-family: 'Courier New', monospace;
            }
        """)
        private_key_layout.addWidget(self.private_key_display)
        key_display_layout.addWidget(private_key_frame)
        
        key_gen_layout.addLayout(key_display_layout)
        
        # Przyciski zapisu kluczy
        save_keys_layout = QHBoxLayout()
        
        self.save_both_keys_btn = QPushButton("💾 Zapisz oba klucze")
        self.save_both_keys_btn.setEnabled(False)
        self.save_both_keys_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #17a2b8, stop:1 #138496);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 12px;
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
        self.save_both_keys_btn.clicked.connect(self.save_key_pair)
        save_keys_layout.addWidget(self.save_both_keys_btn)
        
        self.save_public_key_btn = QPushButton("💾 Zapisz klucz publiczny")
        self.save_public_key_btn.setEnabled(False)
        self.save_public_key_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4caf50, stop:1 #45a049);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #45a049, stop:1 #3d8b40);
            }
            QPushButton:disabled {
                background: #6c757d;
                color: #adb5bd;
            }
        """)
        self.save_public_key_btn.clicked.connect(self.save_public_key)
        save_keys_layout.addWidget(self.save_public_key_btn)
        
        self.save_private_key_btn = QPushButton("💾 Zapisz klucz prywatny")
        self.save_private_key_btn.setEnabled(False)
        self.save_private_key_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f44336, stop:1 #d32f2f);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #d32f2f, stop:1 #b71c1c);
            }
            QPushButton:disabled {
                background: #6c757d;
                color: #adb5bd;
            }
        """)
        self.save_private_key_btn.clicked.connect(self.save_private_key)
        save_keys_layout.addWidget(self.save_private_key_btn)
        
        key_gen_layout.addLayout(save_keys_layout)
        main_layout.addWidget(key_gen_frame)
        
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
        
        input_label = QLabel("📁 Plik do zaszyfrowania:")
        input_label.setStyleSheet("font-weight: bold; color: #2c3e50; margin-bottom: 10px;")
        file_layout.addWidget(input_label)
        
        file_input_layout = QHBoxLayout()
        self.input_file_path = QLineEdit()
        self.input_file_path.setPlaceholderText("Wybierz plik do zaszyfrowania...")
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
        self.output_file_path.setPlaceholderText("Wybierz lokalizację zapisu zaszyfrowanego pliku...")
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
                    stop:0 #f39c12, stop:1 #e67e22);
                border-radius: 6px;
            }
        """)
        main_layout.addWidget(self.progress_bar)
        
        # Przyciski
        button_layout = QHBoxLayout()
        
        self.encrypt_button = QPushButton("🔐 Szyfruj plik")
        self.encrypt_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f39c12, stop:1 #e67e22);
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
                    stop:0 #e67e22, stop:1 #d35400);
            }
            QPushButton:disabled {
                background: #6c757d;
                color: #adb5bd;
            }
        """)
        self.encrypt_button.clicked.connect(self.encrypt_file)
        self.encrypt_button.setEnabled(False)
        button_layout.addWidget(self.encrypt_button)
        
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
        
        app_logger.info("RSA encrypt file window initialized")
    
    def get_key_size(self):
        """Pobiera rozmiar klucza z combobox"""
        selection = self.key_size_combo.currentText()
        if "512" in selection:
            return 512
        elif "1024" in selection:
            return 1024
        elif "2048" in selection:
            return 2048
        return 1024
    
    def generate_keys(self):
        """Generuje parę kluczy RSA"""
        try:
            self.generate_key_btn.setEnabled(False)
            self.generate_key_btn.setText("⏳ Generowanie kluczy...")
            
            key_size = self.get_key_size()
            
            self.key_gen_worker = RSAFileKeyGenWorker(key_size)
            self.key_gen_worker.finished.connect(self.on_keys_generated)
            self.key_gen_worker.error.connect(self.on_key_gen_error)
            self.key_gen_worker.start()
            
            app_logger.info(f"RSA key generation started with key size {key_size}")
            
        except Exception as e:
            app_logger.error(f"RSA key generation error: {str(e)}")
            QMessageBox.critical(self, "Błąd", f"Wystąpił błąd podczas generowania kluczy:\n{str(e)}")
            self.generate_key_btn.setEnabled(True)
            self.generate_key_btn.setText("🔑 Generuj parę kluczy")
    
    def on_keys_generated(self, key_pair):
        """Obsługuje zakończenie generowania kluczy"""
        try:
            self.public_key, self.private_key = key_pair
            
            # Wyświetl klucze
            self.public_key_display.setPlainText(f"({self.public_key[0]}, {self.public_key[1]})")
            self.private_key_display.setPlainText(f"({self.private_key[0]}, {self.private_key[1]})")
            
            self.encrypt_button.setEnabled(True)
            self.save_both_keys_btn.setEnabled(True)
            self.save_public_key_btn.setEnabled(True)
            self.save_private_key_btn.setEnabled(True)
            self.generate_key_btn.setEnabled(True)
            self.generate_key_btn.setText("🔑 Generuj parę kluczy")
            
            QMessageBox.information(
                self, 
                "Sukces", 
                "Para kluczy RSA została wygenerowana pomyślnie!\n\n"
                "⚠️ WAŻNE: Zapisz klucz prywatny w bezpiecznym miejscu!\n"
                "Będzie potrzebny do deszyfrowania.\n\n"
                "💡 Możesz użyć przycisków poniżej, aby zapisać klucze do plików."
            )
            
            app_logger.info("RSA key pair generated successfully")
            
        except Exception as e:
            app_logger.error(f"RSA key generation finish error: {str(e)}")
            QMessageBox.critical(self, "Błąd", f"Wystąpił błąd:\n{str(e)}")
            self.generate_key_btn.setEnabled(True)
            self.generate_key_btn.setText("🔑 Generuj parę kluczy")
    
    def on_key_gen_error(self, error_msg):
        """Obsługuje błąd generowania kluczy"""
        app_logger.error(f"RSA key generation error: {error_msg}")
        QMessageBox.critical(self, "Błąd generowania kluczy", f"Wystąpił błąd podczas generowania kluczy:\n{error_msg}")
        self.generate_key_btn.setEnabled(True)
        self.generate_key_btn.setText("🔑 Generuj parę kluczy")
    
    def browse_input_file(self):
        """Otwiera dialog wyboru pliku wejściowego"""
        try:
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Wybierz plik do zaszyfrowania",
                "",
                "Wszystkie pliki (*.*)"
            )
            if file_path:
                self.input_file_path.setText(file_path)
                # Automatyczne ustawienie ścieżki wyjściowej
                base_name = os.path.splitext(file_path)[0]
                self.output_file_path.setText(f"{base_name}_encrypted.rsa")
                app_logger.info(f"Input file selected: {file_path}")
        except Exception as e:
            app_logger.error(f"Browse input file error: {str(e)}")
            QMessageBox.critical(self, "Błąd", f"Wystąpił błąd podczas wyboru pliku:\n{str(e)}")
    
    def browse_output_file(self):
        """Otwiera dialog wyboru pliku wyjściowego"""
        try:
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Wybierz lokalizację zapisu zaszyfrowanego pliku",
                "",
                "Pliki RSA (*.rsa);;Wszystkie pliki (*.*)"
            )
            if file_path:
                self.output_file_path.setText(file_path)
                app_logger.info(f"Output file selected: {file_path}")
        except Exception as e:
            app_logger.error(f"Browse output file error: {str(e)}")
            QMessageBox.critical(self, "Błąd", f"Wystąpił błąd podczas wyboru lokalizacji:\n{str(e)}")
    
    def encrypt_file(self):
        """Szyfruje plik"""
        try:
            if not self.public_key:
                QMessageBox.warning(self, "Błąd", "Najpierw wygeneruj parę kluczy!")
                return
            
            input_file = self.input_file_path.text().strip()
            output_file = self.output_file_path.text().strip()
            
            if not input_file:
                QMessageBox.warning(self, "Błąd", "Wybierz plik do zaszyfrowania!")
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
            
            # Wyłączenie przycisku podczas szyfrowania
            self.encrypt_button.setEnabled(False)
            self.encrypt_button.setText("⏳ Szyfrowanie...")
            self.progress_bar.setVisible(True)
            self.progress_bar.setValue(0)
            
            # Uruchomienie wątku szyfrowania
            self.worker = RSAFileEncryptWorker(input_file, output_file, self.public_key, self.get_key_size())
            self.worker.finished.connect(self.on_encryption_finished)
            self.worker.error.connect(self.on_encryption_error)
            self.worker.progress.connect(self.progress_bar.setValue)
            self.worker.start()
            
            app_logger.info(f"RSA file encryption started: {input_file} -> {output_file}")
            
        except Exception as e:
            app_logger.error(f"RSA file encryption error: {str(e)}")
            QMessageBox.critical(self, "Błąd", f"Wystąpił błąd podczas szyfrowania:\n{str(e)}")
            self.encrypt_button.setEnabled(True)
            self.encrypt_button.setText("🔐 Szyfruj plik")
            self.progress_bar.setVisible(False)
    
    def on_encryption_finished(self, success):
        """Obsługuje zakończenie szyfrowania"""
        try:
            self.encrypt_button.setEnabled(True)
            self.encrypt_button.setText("🔐 Szyfruj plik")
            self.progress_bar.setVisible(False)
            
            if success:
                app_logger.info("RSA file encryption completed successfully")
                QMessageBox.information(
                    self, 
                    "Sukces", 
                    f"Plik został zaszyfrowany pomyślnie!\n\n"
                    f"Zaszyfrowany plik: {self.output_file_path.text()}\n\n"
                    f"⚠️ Pamiętaj o zapisaniu klucza prywatnego do deszyfrowania!"
                )
            else:
                app_logger.error("RSA file encryption failed")
                QMessageBox.critical(self, "Błąd", "Szyfrowanie pliku nie powiodło się!")
            
        except Exception as e:
            app_logger.error(f"RSA encryption finish error: {str(e)}")
            QMessageBox.critical(self, "Błąd", f"Wystąpił błąd:\n{str(e)}")
            self.encrypt_button.setEnabled(True)
            self.encrypt_button.setText("🔐 Szyfruj plik")
            self.progress_bar.setVisible(False)
    
    def on_encryption_error(self, error_msg):
        """Obsługuje błąd szyfrowania"""
        app_logger.error(f"RSA file encryption error: {error_msg}")
        QMessageBox.critical(self, "Błąd szyfrowania", f"Wystąpił błąd podczas szyfrowania:\n{error_msg}")
        self.encrypt_button.setEnabled(True)
        self.encrypt_button.setText("🔐 Szyfruj plik")
        self.progress_bar.setVisible(False)
    
    def save_key_pair(self):
        """Zapisuje parę kluczy do pliku"""
        try:
            if not self.public_key or not self.private_key:
                QMessageBox.warning(self, "Błąd", "Najpierw wygeneruj parę kluczy!")
                return
            
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Zapisz parę kluczy RSA",
                "",
                "Pliki JSON (*.json);;Wszystkie pliki (*.*)"
            )
            
            if file_path:
                if rsa_save_key_pair(self.public_key, self.private_key, file_path, self.get_key_size()):
                    QMessageBox.information(self, "Sukces", f"Para kluczy została zapisana do:\n{file_path}")
                    app_logger.info(f"RSA key pair saved to {file_path}")
                else:
                    QMessageBox.critical(self, "Błąd", "Nie udało się zapisać kluczy!")
                    
        except Exception as e:
            app_logger.error(f"Save key pair error: {str(e)}")
            QMessageBox.critical(self, "Błąd", f"Wystąpił błąd podczas zapisywania:\n{str(e)}")
    
    def save_public_key(self):
        """Zapisuje tylko klucz publiczny do pliku"""
        try:
            if not self.public_key:
                QMessageBox.warning(self, "Błąd", "Najpierw wygeneruj parę kluczy!")
                return
            
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Zapisz klucz publiczny RSA",
                "",
                "Pliki JSON (*.json);;Wszystkie pliki (*.*)"
            )
            
            if file_path:
                if rsa_save_public_key(self.public_key, file_path, self.get_key_size()):
                    QMessageBox.information(self, "Sukces", f"Klucz publiczny został zapisany do:\n{file_path}")
                    app_logger.info(f"RSA public key saved to {file_path}")
                else:
                    QMessageBox.critical(self, "Błąd", "Nie udało się zapisać klucza!")
                    
        except Exception as e:
            app_logger.error(f"Save public key error: {str(e)}")
            QMessageBox.critical(self, "Błąd", f"Wystąpił błąd podczas zapisywania:\n{str(e)}")
    
    def save_private_key(self):
        """Zapisuje tylko klucz prywatny do pliku"""
        try:
            if not self.private_key:
                QMessageBox.warning(self, "Błąd", "Najpierw wygeneruj parę kluczy!")
                return
            
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Zapisz klucz prywatny RSA",
                "",
                "Pliki JSON (*.json);;Wszystkie pliki (*.*)"
            )
            
            if file_path:
                if rsa_save_private_key(self.private_key, file_path, self.get_key_size()):
                    QMessageBox.information(
                        self, 
                        "Sukces", 
                        f"Klucz prywatny został zapisany do:\n{file_path}\n\n"
                        f"⚠️ WAŻNE: Przechowuj ten plik w bezpiecznym miejscu!"
                    )
                    app_logger.info(f"RSA private key saved to {file_path}")
                else:
                    QMessageBox.critical(self, "Błąd", "Nie udało się zapisać klucza!")
                    
        except Exception as e:
            app_logger.error(f"Save private key error: {str(e)}")
            QMessageBox.critical(self, "Błąd", f"Wystąpił błąd podczas zapisywania:\n{str(e)}")
    
    def clear_all(self):
        """Czyści wszystkie pola"""
        try:
            self.input_file_path.clear()
            self.output_file_path.clear()
            self.public_key_display.clear()
            self.private_key_display.clear()
            self.public_key = None
            self.private_key = None
            self.encrypt_button.setEnabled(False)
            self.save_both_keys_btn.setEnabled(False)
            self.save_public_key_btn.setEnabled(False)
            self.save_private_key_btn.setEnabled(False)
            self.progress_bar.setVisible(False)
            app_logger.info("RSA encrypt file window cleared")
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
    window = RSAEncryptFileWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

