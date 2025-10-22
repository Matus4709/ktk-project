#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Okno szyfrowania tekstu szyfrem Vigenère
"""

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QTextEdit, QLineEdit, 
                             QMessageBox, QApplication)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from utils.vigenere_cipher import vigenere_encrypt
from utils.logger import app_logger


class EncryptTextVigenereWindow(QMainWindow):
    """Okno szyfrowania tekstu szyfrem Vigenère"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        app_logger.log_window_open("EncryptTextVigenereWindow")
        self.init_ui()
        self.setup_styles()
        
    def init_ui(self):
        """Inicjalizacja interfejsu okna szyfrowania"""
        self.setWindowTitle("Szyfrowanie Tekstu - Vigenère")
        self.setGeometry(200, 200, 600, 500)
        self.setMinimumSize(500, 400)
        self.showMaximized()
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Tytuł
        title = QLabel("🔑 Szyfrowanie Tekstu - Vigenère")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setStyleSheet("""
            QLabel {
                color: #9b59b6;
                padding: 10px;
                background: white;
                border-radius: 10px;
                border: 2px solid #9b59b6;
            }
        """)
        layout.addWidget(title)
        
        # Pole na tekst do szyfrowania
        text_label = QLabel("Tekst do szyfrowania:")
        text_label.setFont(QFont("Arial", 12, QFont.Bold))
        layout.addWidget(text_label)
        
        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText("Wprowadź tekst do szyfrowania...")
        self.text_input.setMaximumHeight(120)
        self.text_input.setStyleSheet("""
            QTextEdit {
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                padding: 10px;
                font-size: 12px;
                background: white;
            }
            QTextEdit:focus {
                border-color: #3498db;
            }
        """)
        layout.addWidget(self.text_input)
        
        # Pole klucza
        key_label = QLabel("Klucz szyfrowania:")
        key_label.setFont(QFont("Arial", 12, QFont.Bold))
        layout.addWidget(key_label)
        
        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("Wprowadź klucz (tylko litery)...")
        self.key_input.setText("SECRET")
        self.key_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                padding: 10px;
                font-size: 12px;
                background: white;
                max-width: 200px;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
        """)
        layout.addWidget(self.key_input)
        
        # Przyciski
        buttons_layout = QHBoxLayout()
        
        self.encrypt_btn = QPushButton("🔑 Szyfruj")
        self.encrypt_btn.setMinimumSize(120, 40)
        self.encrypt_btn.setFont(QFont("Arial", 12, QFont.Bold))
        self.encrypt_btn.setStyleSheet("""
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
        self.encrypt_btn.clicked.connect(self.encrypt_text)
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
        
        # Wynik szyfrowania
        result_label = QLabel("Zaszyfrowany tekst:")
        result_label.setFont(QFont("Arial", 12, QFont.Bold))
        layout.addWidget(result_label)
        
        self.result_output = QTextEdit()
        self.result_output.setReadOnly(True)
        self.result_output.setMaximumHeight(120)
        self.result_output.setStyleSheet("""
            QTextEdit {
                border: 2px solid #9b59b6;
                border-radius: 8px;
                padding: 10px;
                font-size: 12px;
                background: #f8f9fa;
            }
        """)
        layout.addWidget(self.result_output)
        
        # Przycisk kopiowania
        self.copy_btn = QPushButton("📋 Kopiuj wynik")
        self.copy_btn.setMinimumSize(150, 40)
        self.copy_btn.setFont(QFont("Arial", 12, QFont.Bold))
        self.copy_btn.setStyleSheet("""
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
        self.copy_btn.clicked.connect(self.copy_result)
        layout.addWidget(self.copy_btn)
        
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
        """Ustawienie stylów okna szyfrowania"""
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #ecf0f1, stop:1 #bdc3c7);
            }
        """)
        
    def encrypt_text(self):
        """Szyfruje wprowadzony tekst szyfrem Vigenère"""
        text = self.text_input.toPlainText().strip()
        if not text:
            app_logger.log_validation_error("tekst", "pusty tekst")
            QMessageBox.warning(self, "Błąd", "Wprowadź tekst do szyfrowania!")
            return
            
        key = self.key_input.text().strip()
        if not key:
            app_logger.log_validation_error("klucz", "pusty klucz")
            QMessageBox.warning(self, "Błąd", "Wprowadź klucz szyfrowania!")
            return
            
        try:
            app_logger.log_encryption_start("tekst Vigenère", f"klucz: {key}")
            encrypted_text = vigenere_encrypt(text, key)
            app_logger.log_encryption_success("tekst Vigenère", len(encrypted_text))
            
            # Wyświetl zaszyfrowany tekst
            self.result_output.setPlainText(encrypted_text)
            
            QMessageBox.information(self, "Sukces", 
                f"Tekst został zaszyfrowany szyfrem Vigenère z kluczem '{key}'!")
            
        except ValueError as e:
            app_logger.log_validation_error("klucz", str(e))
            QMessageBox.warning(self, "Błąd", f"Błąd klucza: {str(e)}")
        except Exception as e:
            app_logger.log_error("szyfrowanie tekstu Vigenère", str(e))
            QMessageBox.critical(self, "Błąd", f"Wystąpił błąd podczas szyfrowania: {str(e)}")
            
    def clear_fields(self):
        """Czyści wszystkie pola"""
        self.text_input.clear()
        self.key_input.setText("SECRET")
        self.result_output.clear()
        
    def copy_result(self):
        """Kopiuje wynik do schowka"""
        result = self.result_output.toPlainText()
        if result:
            clipboard = QApplication.clipboard()
            clipboard.setText(result)
            QMessageBox.information(self, "Sukces", "Wynik został skopiowany do schowka!")
        else:
            QMessageBox.warning(self, "Błąd", "Brak wyniku do skopiowania!")
            
    def go_back(self):
        """Powrót do okna wyboru"""
        if self.parent:
            self.parent.show()
        self.close()





