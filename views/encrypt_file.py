#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Okno szyfrowania pliku
"""

import os
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QLineEdit, QFileDialog, 
                             QMessageBox, QApplication, QTextEdit)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from utils.crypto_utils import encrypt_file


class EncryptFileWindow(QMainWindow):
    """Okno szyfrowania pliku"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()
        self.setup_styles()
        
    def init_ui(self):
        """Inicjalizacja interfejsu okna szyfrowania pliku"""
        self.setWindowTitle("Szyfrowanie Pliku")
        self.setGeometry(200, 200, 600, 500)
        self.setMinimumSize(500, 400)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Tytuł
        title = QLabel("🔒 Szyfrowanie Pliku")
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
        
        # Wybór pliku do szyfrowania
        file_label = QLabel("Plik do szyfrowania:")
        file_label.setFont(QFont("Arial", 12, QFont.Bold))
        layout.addWidget(file_label)
        
        file_layout = QHBoxLayout()
        
        self.file_input = QLineEdit()
        self.file_input.setPlaceholderText("Wybierz plik do szyfrowania...")
        self.file_input.setReadOnly(True)
        self.file_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                padding: 10px;
                font-size: 12px;
                background: white;
            }
        """)
        file_layout.addWidget(self.file_input)
        
        self.browse_btn = QPushButton("📁 Przeglądaj")
        self.browse_btn.setMinimumSize(120, 40)
        self.browse_btn.setFont(QFont("Arial", 12, QFont.Bold))
        self.browse_btn.setStyleSheet("""
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
        self.browse_btn.clicked.connect(self.browse_file)
        file_layout.addWidget(self.browse_btn)
        
        layout.addLayout(file_layout)
        
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
        
        self.encrypt_btn = QPushButton("🔒 Szyfruj plik")
        self.encrypt_btn.setMinimumSize(150, 40)
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
        
        # Wynik szyfrowania
        result_label = QLabel("Informacje o szyfrowaniu:")
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
        
    def browse_file(self):
        """Otwiera dialog wyboru pliku"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Wybierz plik do szyfrowania", 
            "", 
            "Wszystkie pliki (*.*)"
        )
        if file_path:
            self.file_input.setText(file_path)
            
    def encrypt_file(self):
        """Szyfruje wybrany plik"""
        file_path = self.file_input.text().strip()
        if not file_path:
            QMessageBox.warning(self, "Błąd", "Wybierz plik do szyfrowania!")
            return
            
        if not os.path.exists(file_path):
            QMessageBox.warning(self, "Błąd", "Wybrany plik nie istnieje!")
            return
            
        try:
            # Wybierz lokalizację zapisu
            output_path, _ = QFileDialog.getSaveFileName(
                self, 
                "Zapisz zaszyfrowany plik jako", 
                file_path + ".encrypted", 
                "Wszystkie pliki (*.*)"
            )
            
            if not output_path:
                return
                
            password = self.password_input.text().strip()
            success, result = encrypt_file(file_path, output_path, password if password else None)
            
            if success:
                self.result_output.setPlainText(
                    f"Plik został zaszyfrowany pomyślnie!\n"
                    f"Oryginalny plik: {os.path.basename(file_path)}\n"
                    f"Zaszyfrowany plik: {os.path.basename(output_path)}\n"
                    f"Lokalizacja: {output_path}"
                )
                
                if not password:
                    # Zapisz klucz do schowka
                    clipboard = QApplication.clipboard()
                    clipboard.setText(f"Klucz: {result}")
                    QMessageBox.information(self, "Sukces", 
                        "Plik został zaszyfrowany pomyślnie!\nKlucz został skopiowany do schowka.")
                else:
                    QMessageBox.information(self, "Sukces", "Plik został zaszyfrowany pomyślnie!")
            else:
                QMessageBox.critical(self, "Błąd", f"Wystąpił błąd podczas szyfrowania: {result}")
                
        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Wystąpił błąd podczas szyfrowania: {str(e)}")
            
    def clear_fields(self):
        """Czyści wszystkie pola"""
        self.file_input.clear()
        self.password_input.clear()
        self.result_output.clear()
        
    def go_back(self):
        """Powrót do okna wyboru"""
        if self.parent:
            self.parent.show()
        self.close()
