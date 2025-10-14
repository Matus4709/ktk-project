#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Okno wyboru typu szyfrowania
"""

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QFrame, QGridLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class CipherChoiceWindow(QMainWindow):
    """Okno wyboru typu szyfrowania"""
    
    def __init__(self, parent=None, operation_type="encrypt", data_type="text"):
        super().__init__(parent)
        self.parent = parent
        self.operation_type = operation_type  # "encrypt" lub "decrypt"
        self.data_type = data_type  # "text" lub "file"
        self.init_ui()
        self.setup_styles()
        
    def init_ui(self):
        """Inicjalizacja interfejsu użytkownika"""
        operation_name = "Szyfrowanie" if self.operation_type == "encrypt" else "Deszyfrowanie"
        data_name = "Tekstu" if self.data_type == "text" else "Pliku"
        
        self.setWindowTitle(f"{operation_name} {data_name} - Wybór szyfru")
        self.setGeometry(150, 150, 600, 500)
        self.setMinimumSize(500, 400)
        self.showMaximized()
        
        # Centralny widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Główny layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # Tytuł
        icon = "🔒" if self.operation_type == "encrypt" else "🔓"
        data_icon = "📝" if self.data_type == "text" else "📁"
        title_label = QLabel(f"{icon} {operation_name} {data_name}")
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
        
        # Ramka z opcjami szyfrowania
        options_frame = QFrame()
        options_frame.setFrameStyle(QFrame.StyledPanel)
        options_frame.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 15px;
            }
        """)
        options_layout = QGridLayout(options_frame)
        options_layout.setSpacing(30)
        options_layout.setContentsMargins(40, 30, 40, 30)
        
        # Szyfr Cezara
        self.caesar_btn = QPushButton("Szyfr Cezara")
        self.caesar_btn.setMinimumSize(200, 150)
        self.caesar_btn.setFont(QFont("Arial", 16, QFont.Bold))
        self.caesar_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #27ae60, stop:1 #229954);
                color: white;
                border: none;
                border-radius: 15px;
                padding: 20px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #229954, stop:1 #1e8449);
                transform: scale(1.05);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #1e8449, stop:1 #196f3d);
            }
        """)
        self.caesar_btn.clicked.connect(self.open_caesar_window)
        options_layout.addWidget(self.caesar_btn, 0, 0)
        
        # Szyfr Vigenère
        self.vigenere_btn = QPushButton("Szyfr Vigenère")
        self.vigenere_btn.setMinimumSize(200, 150)
        self.vigenere_btn.setFont(QFont("Arial", 16, QFont.Bold))
        self.vigenere_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #9b59b6, stop:1 #8e44ad);
                color: white;
                border: none;
                border-radius: 15px;
                padding: 20px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #8e44ad, stop:1 #7d3c98);
                transform: scale(1.05);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #7d3c98, stop:1 #6c3483);
            }
        """)
        self.vigenere_btn.clicked.connect(self.open_vigenere_window)
        options_layout.addWidget(self.vigenere_btn, 0, 1)
        
        # Szyfr z kluczem bieżącym
        self.stream_btn = QPushButton("Szyfr z kluczem\nbieżącym")
        self.stream_btn.setMinimumSize(200, 150)
        self.stream_btn.setFont(QFont("Arial", 16, QFont.Bold))
        self.stream_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #e67e22, stop:1 #d35400);
                color: white;
                border: none;
                border-radius: 15px;
                padding: 20px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #d35400, stop:1 #ba4a00);
                transform: scale(1.05);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #ba4a00, stop:1 #a04000);
            }
        """)
        self.stream_btn.clicked.connect(self.open_stream_window)
        options_layout.addWidget(self.stream_btn, 0, 2)
        
        # # Opcja AES (wkrótce)
        # aes_option_layout = QHBoxLayout()
        
        # self.aes_btn = QPushButton("🔐 AES (wkrótce)")
        # self.aes_btn.setMinimumSize(200, 80)
        # self.aes_btn.setFont(QFont("Arial", 14, QFont.Bold))
        # self.aes_btn.setStyleSheet("""
        #     QPushButton {
        #         background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
        #             stop:0 #95a5a6, stop:1 #7f8c8d);
        #         color: white;
        #         border: none;
        #         border-radius: 15px;
        #         padding: 15px;
        #     }
        #     QPushButton:hover {
        #         background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
        #             stop:0 #7f8c8d, stop:1 #6c7b7d);
        #     }
        # """)
        # self.aes_btn.clicked.connect(self.show_coming_soon)
        # aes_option_layout.addWidget(self.aes_btn)
        
        # aes_desc = QLabel("Zaawansowane szyfrowanie AES - w przygotowaniu")
        # aes_desc.setFont(QFont("Arial", 10))
        # aes_desc.setStyleSheet("QLabel { color: #7f8c8d; }")
        # aes_desc.setWordWrap(True)
        # aes_option_layout.addWidget(aes_desc)
        
        # options_layout.addLayout(aes_option_layout)
        
        # # Opcja RSA (wkrótce)
        # rsa_option_layout = QHBoxLayout()
        
        # self.rsa_btn = QPushButton("🔑 RSA (wkrótce)")
        # self.rsa_btn.setMinimumSize(200, 80)
        # self.rsa_btn.setFont(QFont("Arial", 14, QFont.Bold))
        # self.rsa_btn.setStyleSheet("""
        #     QPushButton {
        #         background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
        #             stop:0 #95a5a6, stop:1 #7f8c8d);
        #         color: white;
        #         border: none;
        #         border-radius: 15px;
        #         padding: 15px;
        #     }
        #     QPushButton:hover {
        #         background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
        #             stop:0 #7f8c8d, stop:1 #6c7b7d);
        #     }
        # """)
        # self.rsa_btn.clicked.connect(self.show_coming_soon)
        # rsa_option_layout.addWidget(self.rsa_btn)
        
        # rsa_desc = QLabel("Szyfrowanie asymetryczne RSA - w przygotowaniu")
        # rsa_desc.setFont(QFont("Arial", 10))
        # rsa_desc.setStyleSheet("QLabel { color: #7f8c8d; }")
        # rsa_desc.setWordWrap(True)
        # rsa_option_layout.addWidget(rsa_desc)
        
        # options_layout.addLayout(rsa_option_layout)
        
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
        
    def open_caesar_window(self):
        """Otwiera okno szyfrowania/deszyfrowania szyfrem Cezara"""
        if self.data_type == "text":
            if self.operation_type == "encrypt":
                from .encrypt_text import EncryptTextWindow
                self.cipher_window = EncryptTextWindow(self)
            else:
                from .decrypt_text import DecryptTextWindow
                self.cipher_window = DecryptTextWindow(self)
        else:  # file
            if self.operation_type == "encrypt":
                from .encrypt_file import EncryptFileWindow
                self.cipher_window = EncryptFileWindow(self)
            else:
                from .decrypt_file import DecryptFileWindow
                self.cipher_window = DecryptFileWindow(self)
        
        self.cipher_window.show()
        self.hide()
        
    def open_vigenere_window(self):
        """Otwiera okno szyfrowania/deszyfrowania szyfrem Vigenère"""
        if self.data_type == "text":
            if self.operation_type == "encrypt":
                from .encrypt_text_vigenere import EncryptTextVigenereWindow
                self.cipher_window = EncryptTextVigenereWindow(self)
            else:
                from .decrypt_text_vigenere import DecryptTextVigenereWindow
                self.cipher_window = DecryptTextVigenereWindow(self)
        else:  # file
            if self.operation_type == "encrypt":
                from .encrypt_file_vigenere import EncryptFileVigenereWindow
                self.cipher_window = EncryptFileVigenereWindow(self)
            else:
                from .decrypt_file_vigenere import DecryptFileVigenereWindow
                self.cipher_window = DecryptFileVigenereWindow(self)
        
        self.cipher_window.show()
        self.hide()
        
    def open_stream_window(self):
        """Otwiera okno szyfrowania/deszyfrowania szyfrem z kluczem bieżącym"""
        if self.data_type == "text":
            if self.operation_type == "encrypt":
                from .encrypt_text_stream import EncryptTextStreamWindow
                self.cipher_window = EncryptTextStreamWindow(self)
            else:
                from .decrypt_text_stream import DecryptTextStreamWindow
                self.cipher_window = DecryptTextStreamWindow(self)
        else:  # file
            if self.operation_type == "encrypt":
                from .encrypt_file_stream import EncryptFileStreamWindow
                self.cipher_window = EncryptFileStreamWindow(self)
            else:
                from .decrypt_file_stream import DecryptFileStreamWindow
                self.cipher_window = DecryptFileStreamWindow(self)
        
        self.cipher_window.show()
        self.hide()
        
    def show_coming_soon(self):
        """Pokazuje komunikat o nadchodzących funkcjach"""
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.information(self, "Wkrótce", 
            "Ta funkcja będzie dostępna w następnej wersji aplikacji!")
        
    def go_back(self):
        """Powrót do okna wyboru typu"""
        if self.parent:
            self.parent.show()
        self.close()
