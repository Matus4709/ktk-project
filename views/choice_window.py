#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Okno wyboru między szyfrowaniem/deszyfrowaniem tekstu a pliku
"""

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class ChoiceWindow(QMainWindow):
    """Okno wyboru między tekstem a plikiem"""
    
    def __init__(self, parent=None, operation_type="encrypt"):
        super().__init__(parent)
        self.parent = parent
        self.operation_type = operation_type  # "encrypt" lub "decrypt"
        self.init_ui()
        self.setup_styles()
        
    def init_ui(self):
        """Inicjalizacja interfejsu użytkownika"""
        operation_name = "Szyfrowanie" if self.operation_type == "encrypt" else "Deszyfrowanie"
        self.setWindowTitle(f"{operation_name} - Wybór typu")
        self.setGeometry(150, 150, 500, 400)
        self.setMinimumSize(400, 300)
        
        # Centralny widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Główny layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # Tytuł
        icon = "🔒" if self.operation_type == "encrypt" else "🔓"
        title_label = QLabel(f"{icon} {operation_name}")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 20, QFont.Bold))
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
        
        # Ramka z opcjami
        options_frame = QFrame()
        options_frame.setFrameStyle(QFrame.StyledPanel)
        options_frame.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 15px;
                border: 2px solid #bdc3c7;
            }
        """)
        options_layout = QVBoxLayout(options_frame)
        options_layout.setSpacing(20)
        options_layout.setContentsMargins(40, 30, 40, 30)
        
        # Opcja tekst
        text_option_layout = QHBoxLayout()
        
        self.text_btn = QPushButton("📝 Tekst")
        self.text_btn.setMinimumSize(150, 80)
        self.text_btn.setFont(QFont("Arial", 14, QFont.Bold))
        self.text_btn.setStyleSheet("""
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
        self.text_btn.clicked.connect(self.open_text_window)
        text_option_layout.addWidget(self.text_btn)
        
        text_desc = QLabel("Szyfruj/deszyfruj bezpośrednio tekst w aplikacji")
        text_desc.setFont(QFont("Arial", 10))
        text_desc.setStyleSheet("QLabel { color: #7f8c8d; }")
        text_desc.setWordWrap(True)
        text_option_layout.addWidget(text_desc)
        
        options_layout.addLayout(text_option_layout)
        
        # Opcja plik
        file_option_layout = QHBoxLayout()
        
        self.file_btn = QPushButton("📁 Plik")
        self.file_btn.setMinimumSize(150, 80)
        self.file_btn.setFont(QFont("Arial", 14, QFont.Bold))
        self.file_btn.setStyleSheet("""
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
        self.file_btn.clicked.connect(self.open_file_window)
        file_option_layout.addWidget(self.file_btn)
        
        file_desc = QLabel("Szyfruj/deszyfruj pliki z dysku")
        file_desc.setFont(QFont("Arial", 10))
        file_desc.setStyleSheet("QLabel { color: #7f8c8d; }")
        file_desc.setWordWrap(True)
        file_option_layout.addWidget(file_desc)
        
        options_layout.addLayout(file_option_layout)
        
        main_layout.addWidget(options_frame)
        
        # Przycisk powrotu
        back_layout = QHBoxLayout()
        
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
        back_layout.addWidget(self.back_btn)
        
        back_layout.addStretch()
        main_layout.addLayout(back_layout)
        
    def setup_styles(self):
        """Ustawienie stylów okna"""
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #ecf0f1, stop:1 #bdc3c7);
            }
        """)
        
    def open_text_window(self):
        """Otwiera okno szyfrowania/deszyfrowania tekstu"""
        if self.operation_type == "encrypt":
            from .encrypt_text import EncryptTextWindow
            self.text_window = EncryptTextWindow(self)
        else:
            from .decrypt_text import DecryptTextWindow
            self.text_window = DecryptTextWindow(self)
        
        self.text_window.show()
        self.hide()
        
    def open_file_window(self):
        """Otwiera okno szyfrowania/deszyfrowania pliku"""
        if self.operation_type == "encrypt":
            from .encrypt_file import EncryptFileWindow
            self.file_window = EncryptFileWindow(self)
        else:
            from .decrypt_file import DecryptFileWindow
            self.file_window = DecryptFileWindow(self)
        
        self.file_window.show()
        self.hide()
        
    def go_back(self):
        """Powrót do głównego okna"""
        if self.parent:
            self.parent.show()
        self.close()
