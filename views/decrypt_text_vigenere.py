#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Okno deszyfrowania tekstu szyfrem Vigenère
"""

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QTextEdit, QLineEdit, 
                             QMessageBox, QApplication)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from utils.vigenere_cipher import vigenere_decrypt
from utils.logger import app_logger


class DecryptTextVigenereWindow(QMainWindow):
    """Okno deszyfrowania tekstu szyfrem Vigenère"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        app_logger.log_window_open("DecryptTextVigenereWindow")
        self.init_ui()
        self.setup_styles()
        
    def init_ui(self):
        """Inicjalizacja interfejsu okna deszyfrowania"""
        self.setWindowTitle("Deszyfrowanie Tekstu - Vigenère")
        self.setGeometry(250, 250, 600, 500)
        self.setMinimumSize(500, 400)
        self.showMaximized()
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Tytuł
        title = QLabel("🔓 Deszyfrowanie Tekstu - Vigenère")
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
        
        # Pole na zaszyfrowany tekst
        text_label = QLabel("Zaszyfrowany tekst:")
        text_label.setFont(QFont("Arial", 12, QFont.Bold))
        layout.addWidget(text_label)
        
        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText("Wprowadź zaszyfrowany tekst...")
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
        key_label = QLabel("Klucz deszyfrowania:")
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
        
        self.decrypt_btn = QPushButton("🔓 Deszyfruj")
        self.decrypt_btn.setMinimumSize(120, 40)
        self.decrypt_btn.setFont(QFont("Arial", 12, QFont.Bold))
        self.decrypt_btn.setStyleSheet("""
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
        self.decrypt_btn.clicked.connect(self.decrypt_text)
        buttons_layout.addWidget(self.decrypt_btn)
        
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
        
        # Wynik deszyfrowania
        result_label = QLabel("Odszyfrowany tekst:")
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
        """Ustawienie stylów okna deszyfrowania"""
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #ecf0f1, stop:1 #bdc3c7);
            }
        """)
        
    def decrypt_text(self):
        """Deszyfruje wprowadzony tekst szyfrem Vigenère"""
        text = self.text_input.toPlainText().strip()
        if not text:
            app_logger.log_validation_error("tekst", "pusty tekst")
            QMessageBox.warning(self, "Błąd", "Wprowadź zaszyfrowany tekst!")
            return
            
        key = self.key_input.text().strip()
        if not key:
            app_logger.log_validation_error("klucz", "pusty klucz")
            QMessageBox.warning(self, "Błąd", "Wprowadź klucz deszyfrowania!")
            return
            
        try:
            app_logger.log_encryption_start("tekst Vigenère", f"klucz: {key}")
            decrypted_text = vigenere_decrypt(text, key)
            app_logger.log_encryption_success("tekst Vigenère", len(decrypted_text))
            
            # Wyświetl odszyfrowany tekst
            self.result_output.setPlainText(decrypted_text)
            
            QMessageBox.information(self, "Sukces", 
                f"Tekst został odszyfrowany szyfrem Vigenère z kluczem '{key}'!")
            
        except ValueError as e:
            app_logger.log_validation_error("klucz", str(e))
            QMessageBox.warning(self, "Błąd", f"Błąd klucza: {str(e)}")
        except Exception as e:
            app_logger.log_error("deszyfrowanie tekstu Vigenère", str(e))
            QMessageBox.critical(self, "Błąd", f"Wystąpił błąd podczas deszyfrowania: {str(e)}")
            
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




