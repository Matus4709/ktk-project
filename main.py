#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aplikacja desktopowa do szyfrowania i deszyfrowania
Autor: Python Developer
"""

import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QTextEdit, 
                             QLineEdit, QMessageBox, QFileDialog, QFrame)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon, QPalette, QColor
from cryptography.fernet import Fernet
import base64


class CryptoApp(QMainWindow):
    """Główna klasa aplikacji do szyfrowania/deszyfrowania"""
    
    def __init__(self):
        super().__init__()
        self.key = None
        self.init_ui()
        self.setup_styles()
        
    def init_ui(self):
        """Inicjalizacja interfejsu użytkownika"""
        self.setWindowTitle("Aplikacja Szyfrowania/Deszyfrowania")
        self.setGeometry(100, 100, 800, 600)
        self.setMinimumSize(600, 400)
        
        # Centralny widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Główny layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # Tytuł aplikacji
        title_label = QLabel("🔐 Aplikacja Szyfrowania")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 24, QFont.Bold))
        title_label.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                margin: 20px 0;
                padding: 15px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #3498db, stop:1 #2980b9);
                border-radius: 10px;
                color: white;
            }
        """)
        main_layout.addWidget(title_label)
        
        # Przyciski główne
        buttons_frame = QFrame()
        buttons_frame.setFrameStyle(QFrame.StyledPanel)
        buttons_frame.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 15px;
                border: 2px solid #bdc3c7;
            }
        """)
        buttons_layout = QHBoxLayout(buttons_frame)
        buttons_layout.setSpacing(30)
        buttons_layout.setContentsMargins(40, 30, 40, 30)
        
        # Przycisk szyfrowania
        self.encrypt_btn = QPushButton("🔒 Szyfrowanie")
        self.encrypt_btn.setMinimumSize(200, 80)
        self.encrypt_btn.setFont(QFont("Arial", 14, QFont.Bold))
        self.encrypt_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #27ae60, stop:1 #229954);
                color: white;
                border: none;
                border-radius: 15px;
                padding: 15px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #229954, stop:1 #1e8449);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #1e8449, stop:1 #196f3d);
            }
        """)
        self.encrypt_btn.clicked.connect(self.show_encrypt_window)
        buttons_layout.addWidget(self.encrypt_btn)
        
        # Przycisk deszyfrowania
        self.decrypt_btn = QPushButton("🔓 Deszyfrowanie")
        self.decrypt_btn.setMinimumSize(200, 80)
        self.decrypt_btn.setFont(QFont("Arial", 14, QFont.Bold))
        self.decrypt_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #e74c3c, stop:1 #c0392b);
                color: white;
                border: none;
                border-radius: 15px;
                padding: 15px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #c0392b, stop:1 #a93226);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #a93226, stop:1 #922b21);
            }
        """)
        self.decrypt_btn.clicked.connect(self.show_decrypt_window)
        buttons_layout.addWidget(self.decrypt_btn)
        
        main_layout.addWidget(buttons_frame)
        
        # Informacja o aplikacji
        info_label = QLabel("Wybierz opcję aby rozpocząć szyfrowanie lub deszyfrowanie tekstu")
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setFont(QFont("Arial", 12))
        info_label.setStyleSheet("""
            QLabel {
                color: #7f8c8d;
                padding: 10px;
            }
        """)
        main_layout.addWidget(info_label)
        
        # Dodaj elastyczność
        main_layout.addStretch()
        
    def setup_styles(self):
        """Ustawienie stylów aplikacji"""
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #ecf0f1, stop:1 #bdc3c7);
            }
        """)
        
    def show_encrypt_window(self):
        """Pokazuje okno wyboru szyfrowania"""
        from views.choice_window import ChoiceWindow
        self.choice_window = ChoiceWindow(self, "encrypt")
        self.choice_window.show()
        
    def show_decrypt_window(self):
        """Pokazuje okno wyboru deszyfrowania"""
        from views.choice_window import ChoiceWindow
        self.choice_window = ChoiceWindow(self, "decrypt")
        self.choice_window.show()


class EncryptWindow(QMainWindow):
    """Okno szyfrowania"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()
        self.setup_styles()
        
    def init_ui(self):
        """Inicjalizacja interfejsu okna szyfrowania"""
        self.setWindowTitle("Szyfrowanie")
        self.setGeometry(200, 200, 600, 500)
        self.setMinimumSize(500, 400)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Tytuł
        title = QLabel("🔒 Szyfrowanie Tekstu")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setStyleSheet("""
            QLabel {
                color: #27ae60;
                padding: 10px;
                background: white;
                border-radius: 10px;
                border: 2px solid #27ae60;
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
        
        # Pole na hasło
        password_label = QLabel("Hasło (opcjonalne):")
        password_label.setFont(QFont("Arial", 12, QFont.Bold))
        layout.addWidget(password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Wprowadź hasło (opcjonalne)")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                padding: 10px;
                font-size: 12px;
                background: white;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
        """)
        layout.addWidget(self.password_input)
        
        # Przyciski
        buttons_layout = QHBoxLayout()
        
        self.encrypt_btn = QPushButton("🔒 Szyfruj")
        self.encrypt_btn.setMinimumSize(120, 40)
        self.encrypt_btn.setFont(QFont("Arial", 12, QFont.Bold))
        self.encrypt_btn.setStyleSheet("""
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
                border: 2px solid #27ae60;
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
        
    def setup_styles(self):
        """Ustawienie stylów okna szyfrowania"""
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #ecf0f1, stop:1 #bdc3c7);
            }
        """)
        
    def encrypt_text(self):
        """Szyfruje wprowadzony tekst"""
        text = self.text_input.toPlainText().strip()
        if not text:
            QMessageBox.warning(self, "Błąd", "Wprowadź tekst do szyfrowania!")
            return
            
        try:
            # Generuj klucz na podstawie hasła lub losowy
            password = self.password_input.text().strip()
            if password:
                # Użyj hasła do generowania klucza
                key = base64.urlsafe_b64encode(password.encode()[:32].ljust(32, b'0'))
            else:
                # Wygeneruj losowy klucz
                key = Fernet.generate_key()
                
            fernet = Fernet(key)
            encrypted_text = fernet.encrypt(text.encode())
            
            # Wyświetl zaszyfrowany tekst
            self.result_output.setPlainText(encrypted_text.decode())
            
            QMessageBox.information(self, "Sukces", "Tekst został zaszyfrowany pomyślnie!")
            
        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Wystąpił błąd podczas szyfrowania: {str(e)}")
            
    def clear_fields(self):
        """Czyści wszystkie pola"""
        self.text_input.clear()
        self.password_input.clear()
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


class DecryptWindow(QMainWindow):
    """Okno deszyfrowania"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()
        self.setup_styles()
        
    def init_ui(self):
        """Inicjalizacja interfejsu okna deszyfrowania"""
        self.setWindowTitle("Deszyfrowanie")
        self.setGeometry(250, 250, 600, 500)
        self.setMinimumSize(500, 400)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Tytuł
        title = QLabel("🔓 Deszyfrowanie Tekstu")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setStyleSheet("""
            QLabel {
                color: #e74c3c;
                padding: 10px;
                background: white;
                border-radius: 10px;
                border: 2px solid #e74c3c;
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
        
        # Pole na hasło
        password_label = QLabel("Hasło (jeśli używane podczas szyfrowania):")
        password_label.setFont(QFont("Arial", 12, QFont.Bold))
        layout.addWidget(password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Wprowadź hasło (jeśli używane)")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                padding: 10px;
                font-size: 12px;
                background: white;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
        """)
        layout.addWidget(self.password_input)
        
        # Przyciski
        buttons_layout = QHBoxLayout()
        
        self.decrypt_btn = QPushButton("🔓 Deszyfruj")
        self.decrypt_btn.setMinimumSize(120, 40)
        self.decrypt_btn.setFont(QFont("Arial", 12, QFont.Bold))
        self.decrypt_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #e74c3c, stop:1 #c0392b);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #c0392b, stop:1 #a93226);
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
                border: 2px solid #e74c3c;
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
        
    def setup_styles(self):
        """Ustawienie stylów okna deszyfrowania"""
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #ecf0f1, stop:1 #bdc3c7);
            }
        """)
        
    def decrypt_text(self):
        """Deszyfruje wprowadzony tekst"""
        text = self.text_input.toPlainText().strip()
        if not text:
            QMessageBox.warning(self, "Błąd", "Wprowadź zaszyfrowany tekst!")
            return
            
        try:
            password = self.password_input.text().strip()
            if password:
                # Użyj hasła do generowania klucza
                key = base64.urlsafe_b64encode(password.encode()[:32].ljust(32, b'0'))
            else:
                QMessageBox.warning(self, "Błąd", "Wprowadź hasło używane podczas szyfrowania!")
                return
                
            fernet = Fernet(key)
            decrypted_text = fernet.decrypt(text.encode())
            
            # Wyświetl odszyfrowany tekst
            self.result_output.setPlainText(decrypted_text.decode())
            
            QMessageBox.information(self, "Sukces", "Tekst został odszyfrowany pomyślnie!")
            
        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Wystąpił błąd podczas deszyfrowania: {str(e)}")
            
    def clear_fields(self):
        """Czyści wszystkie pola"""
        self.text_input.clear()
        self.password_input.clear()
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


def main():
    """Główna funkcja aplikacji"""
    app = QApplication(sys.argv)
    
    # Ustawienie stylu aplikacji
    app.setStyle('Fusion')
    
    # Utworzenie i wyświetlenie głównego okna
    window = CryptoApp()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
