#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Okno szyfrowania pliku szyfrem z kluczem bieżącym
"""

import os
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QLineEdit, QFileDialog, 
                             QMessageBox, QApplication, QProgressBar, QTextEdit)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont
from utils.stream_cipher import stream_encrypt_file, stream_encrypt_binary_file, generate_random_key, validate_key
from utils.logger import app_logger


class EncryptionThread(QThread):
    """Wątek do szyfrowania pliku w tle"""
    progress = pyqtSignal(int)
    finished = pyqtSignal(bool, str)
    
    def __init__(self, input_file, output_file, key, is_binary=False):
        super().__init__()
        self.input_file = input_file
        self.output_file = output_file
        self.key = key
        self.is_binary = is_binary
        
    def run(self):
        try:
            self.progress.emit(25)
            if self.is_binary:
                success = stream_encrypt_binary_file(self.input_file, self.output_file, self.key)
            else:
                success = stream_encrypt_file(self.input_file, self.output_file, self.key)
            
            self.progress.emit(100)
            self.finished.emit(success, "" if success else "Błąd podczas szyfrowania pliku")
        except Exception as e:
            self.finished.emit(False, str(e))


class EncryptFileStreamWindow(QMainWindow):
    """Okno szyfrowania pliku szyfrem z kluczem bieżącym"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.encryption_thread = None
        app_logger.log_window_open("EncryptFileStreamWindow")
        self.init_ui()
        self.setup_styles()
        
    def init_ui(self):
        """Inicjalizacja interfejsu okna szyfrowania pliku"""
        self.setWindowTitle("Szyfrowanie Pliku - Szyfr z kluczem bieżącym")
        self.setGeometry(200, 200, 700, 600)
        self.setMinimumSize(600, 500)
        self.showMaximized()
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Tytuł
        title = QLabel("🔒 Szyfrowanie Pliku - Szyfr z kluczem bieżącym")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setStyleSheet("""
            QLabel {
                color: #e67e22;
                padding: 10px;
                background: white;
                border-radius: 10px;
                border: 2px solid #e67e22;
            }
        """)
        layout.addWidget(title)
        
        # Wybór pliku wejściowego
        input_label = QLabel("Wybierz plik do szyfrowania:")
        input_label.setFont(QFont("Arial", 12, QFont.Bold))
        layout.addWidget(input_label)
        
        input_layout = QHBoxLayout()
        
        self.input_file_path = QLineEdit()
        self.input_file_path.setPlaceholderText("Kliknij 'Przeglądaj' aby wybrać plik...")
        self.input_file_path.setReadOnly(True)
        self.input_file_path.setStyleSheet("""
            QLineEdit {
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                padding: 10px;
                font-size: 12px;
                background: #f8f9fa;
            }
        """)
        input_layout.addWidget(self.input_file_path)
        
        self.browse_input_btn = QPushButton("📁 Przeglądaj")
        self.browse_input_btn.setMinimumSize(120, 40)
        self.browse_input_btn.setFont(QFont("Arial", 10, QFont.Bold))
        self.browse_input_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #3498db, stop:1 #2980b9);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #2980b9, stop:1 #21618c);
            }
        """)
        self.browse_input_btn.clicked.connect(self.browse_input_file)
        input_layout.addWidget(self.browse_input_btn)
        
        layout.addLayout(input_layout)
        
        # Wybór pliku wyjściowego
        output_label = QLabel("Wybierz lokalizację pliku zaszyfrowanego:")
        output_label.setFont(QFont("Arial", 12, QFont.Bold))
        layout.addWidget(output_label)
        
        output_layout = QHBoxLayout()
        
        self.output_file_path = QLineEdit()
        self.output_file_path.setPlaceholderText("Kliknij 'Zapisz jako' aby wybrać lokalizację...")
        self.output_file_path.setReadOnly(True)
        self.output_file_path.setStyleSheet("""
            QLineEdit {
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                padding: 10px;
                font-size: 12px;
                background: #f8f9fa;
            }
        """)
        output_layout.addWidget(self.output_file_path)
        
        self.browse_output_btn = QPushButton("💾 Zapisz jako")
        self.browse_output_btn.setMinimumSize(120, 40)
        self.browse_output_btn.setFont(QFont("Arial", 10, QFont.Bold))
        self.browse_output_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #27ae60, stop:1 #229954);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #229954, stop:1 #1e8449);
            }
        """)
        self.browse_output_btn.clicked.connect(self.browse_output_file)
        output_layout.addWidget(self.browse_output_btn)
        
        layout.addLayout(output_layout)
        
        # Pole klucza
        key_label = QLabel("Klucz szyfrowania (ziarno):")
        key_label.setFont(QFont("Arial", 12, QFont.Bold))
        layout.addWidget(key_label)
        
        key_layout = QHBoxLayout()
        
        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("Wprowadź klucz szyfrowania (minimum 4 znaki)")
        self.key_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                padding: 10px;
                font-size: 12px;
                background: white;
            }
            QLineEdit:focus {
                border-color: #e67e22;
            }
        """)
        key_layout.addWidget(self.key_input)
        
        self.generate_key_btn = QPushButton("🎲 Generuj losowy klucz")
        self.generate_key_btn.setMinimumSize(180, 40)
        self.generate_key_btn.setFont(QFont("Arial", 10, QFont.Bold))
        self.generate_key_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #9b59b6, stop:1 #8e44ad);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #8e44ad, stop:1 #7d3c98);
            }
        """)
        self.generate_key_btn.clicked.connect(self.generate_random_key)
        key_layout.addWidget(self.generate_key_btn)
        
        layout.addLayout(key_layout)
        
        # Pasek postępu
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                text-align: center;
                background: white;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #e67e22, stop:1 #d35400);
                border-radius: 6px;
            }
        """)
        layout.addWidget(self.progress_bar)
        
        # Przyciski
        buttons_layout = QHBoxLayout()
        
        self.encrypt_btn = QPushButton("🔒 Szyfruj plik")
        self.encrypt_btn.setMinimumSize(150, 40)
        self.encrypt_btn.setFont(QFont("Arial", 12, QFont.Bold))
        self.encrypt_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #e67e22, stop:1 #d35400);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #d35400, stop:1 #ba4a00);
            }
            QPushButton:disabled {
                background: #95a5a6;
            }
        """)
        self.encrypt_btn.clicked.connect(self.encrypt_file)
        buttons_layout.addWidget(self.encrypt_btn)
        
        self.clear_btn = QPushButton("🗑️ Wyczyść")
        self.clear_btn.setMinimumSize(120, 40)
        self.clear_btn.setFont(QFont("Arial", 12, QFont.Bold))
        self.clear_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #95a5a6, stop:1 #7f8c8d);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #7f8c8d, stop:1 #6c7b7d);
            }
        """)
        self.clear_btn.clicked.connect(self.clear_fields)
        buttons_layout.addWidget(self.clear_btn)
        
        layout.addLayout(buttons_layout)
        
        # Informacje o pliku
        self.file_info = QTextEdit()
        self.file_info.setReadOnly(True)
        self.file_info.setMaximumHeight(100)
        self.file_info.setStyleSheet("""
            QTextEdit {
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                padding: 10px;
                font-size: 11px;
                background: #f8f9fa;
                font-family: 'Courier New', monospace;
            }
        """)
        self.file_info.setPlaceholderText("Informacje o wybranym pliku pojawią się tutaj...")
        layout.addWidget(self.file_info)
        
        # Przycisk powrotu
        self.back_btn = QPushButton("⬅️ Powrót")
        self.back_btn.setMinimumSize(120, 40)
        self.back_btn.setFont(QFont("Arial", 12, QFont.Bold))
        self.back_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #95a5a6, stop:1 #7f8c8d);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #7f8c8d, stop:1 #6c7b7d);
            }
        """)
        self.back_btn.clicked.connect(self.go_back)
        layout.addWidget(self.back_btn)
        
    def setup_styles(self):
        """Ustawienie stylów okna szyfrowania pliku"""
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #ecf0f1, stop:1 #bdc3c7);
            }
        """)
        
    def browse_input_file(self):
        """Przeglądanie pliku wejściowego"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Wybierz plik do szyfrowania", 
            "", 
            "Wszystkie pliki (*.*)"
        )
        
        if file_path:
            self.input_file_path.setText(file_path)
            self.update_file_info(file_path)
            app_logger.log_user_action("wybrano plik wejściowy")
            
    def browse_output_file(self):
        """Przeglądanie pliku wyjściowego"""
        input_path = self.input_file_path.text()
        if not input_path:
            QMessageBox.warning(self, "Błąd", "Najpierw wybierz plik wejściowy!")
            return
            
        # Sugeruj nazwę pliku wyjściowego
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        suggested_name = f"{base_name}_encrypted_stream"
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, 
            "Zapisz zaszyfrowany plik jako", 
            suggested_name, 
            "Wszystkie pliki (*.*)"
        )
        
        if file_path:
            self.output_file_path.setText(file_path)
            app_logger.log_user_action("wybrano plik wyjściowy")
            
    def update_file_info(self, file_path):
        """Aktualizuje informacje o pliku"""
        try:
            file_size = os.path.getsize(file_path)
            file_name = os.path.basename(file_path)
            
            # Sprawdź czy to plik binarny
            is_binary = self.is_binary_file(file_path)
            file_type = "binarny" if is_binary else "tekstowy"
            
            info_text = f"""Plik: {file_name}
Rozmiar: {file_size:,} bajtów
Typ: {file_type}
Ścieżka: {file_path}"""
            
            self.file_info.setPlainText(info_text)
            
        except Exception as e:
            self.file_info.setPlainText(f"Błąd podczas odczytu informacji o pliku: {str(e)}")
            
    def is_binary_file(self, file_path):
        """Sprawdza czy plik jest binarny"""
        try:
            with open(file_path, 'rb') as f:
                chunk = f.read(1024)
                # Sprawdź czy zawiera bajty null lub inne znaki binarne
                return b'\0' in chunk or any(byte > 127 for byte in chunk)
        except:
            return True  # W razie wątpliwości traktuj jako binarny
            
    def generate_random_key(self):
        """Generuje losowy klucz"""
        random_key = generate_random_key(16)  # 16 bajtów = 32 znaki hex
        self.key_input.setText(random_key)
        app_logger.log_user_action("wygenerowano losowy klucz")
        
    def encrypt_file(self):
        """Szyfruje wybrany plik"""
        input_file = self.input_file_path.text().strip()
        if not input_file:
            app_logger.log_validation_error("plik", "nie wybrano pliku wejściowego")
            QMessageBox.warning(self, "Błąd", "Wybierz plik do szyfrowania!")
            return
            
        output_file = self.output_file_path.text().strip()
        if not output_file:
            app_logger.log_validation_error("plik", "nie wybrano pliku wyjściowego")
            QMessageBox.warning(self, "Błąd", "Wybierz lokalizację pliku zaszyfrowanego!")
            return
            
        key = self.key_input.text().strip()
        if not validate_key(key):
            app_logger.log_validation_error("klucz", "nieprawidłowy klucz")
            QMessageBox.warning(self, "Błąd", "Klucz musi mieć minimum 4 znaki!")
            return
            
        # Sprawdź czy plik wejściowy istnieje
        if not os.path.exists(input_file):
            QMessageBox.critical(self, "Błąd", "Plik wejściowy nie istnieje!")
            return
            
        # Sprawdź czy katalog wyjściowy istnieje
        output_dir = os.path.dirname(output_file)
        if not os.path.exists(output_dir):
            QMessageBox.critical(self, "Błąd", "Katalog wyjściowy nie istnieje!")
            return
            
        # Sprawdź czy to plik binarny
        is_binary = self.is_binary_file(input_file)
        
        # Pokaż informację o typie pliku
        file_type = "binarny" if is_binary else "tekstowy"
        QMessageBox.information(self, "Informacja", 
            f"Plik zostanie zaszyfrowany jako plik {file_type}.\n"
            f"Klucz: {key[:8]}...")
        
        try:
            app_logger.log_encryption_start("plik", "stream cipher")
            
            # Uruchom szyfrowanie w osobnym wątku
            self.encryption_thread = EncryptionThread(input_file, output_file, key, is_binary)
            self.encryption_thread.progress.connect(self.progress_bar.setValue)
            self.encryption_thread.finished.connect(self.encryption_finished)
            
            # Zablokuj przyciski podczas szyfrowania
            self.encrypt_btn.setEnabled(False)
            self.browse_input_btn.setEnabled(False)
            self.browse_output_btn.setEnabled(False)
            self.progress_bar.setVisible(True)
            self.progress_bar.setValue(0)
            
            self.encryption_thread.start()
            
        except Exception as e:
            app_logger.log_error("szyfrowanie pliku", str(e))
            QMessageBox.critical(self, "Błąd", f"Wystąpił błąd podczas szyfrowania: {str(e)}")
            
    def encryption_finished(self, success, error_message):
        """Wywoływane po zakończeniu szyfrowania"""
        # Odblokuj przyciski
        self.encrypt_btn.setEnabled(True)
        self.browse_input_btn.setEnabled(True)
        self.browse_output_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        
        if success:
            app_logger.log_encryption_success("plik", "stream cipher")
            QMessageBox.information(self, "Sukces", 
                "Plik został zaszyfrowany szyfrem z kluczem bieżącym!")
        else:
            app_logger.log_error("szyfrowanie pliku", error_message)
            QMessageBox.critical(self, "Błąd", f"Wystąpił błąd podczas szyfrowania: {error_message}")
            
    def clear_fields(self):
        """Czyści wszystkie pola"""
        self.input_file_path.clear()
        self.output_file_path.clear()
        self.key_input.clear()
        self.file_info.clear()
        self.progress_bar.setVisible(False)
        self.progress_bar.setValue(0)
        
    def go_back(self):
        """Powrót do okna wyboru"""
        if self.parent:
            self.parent.show()
        self.close()
