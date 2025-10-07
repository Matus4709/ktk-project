#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aplikacja desktopowa do szyfrowania i deszyfrowania
Autor: Python Developer
"""

import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from utils.logger import app_logger


class CryptoApp(QMainWindow):
    """Główna klasa aplikacji do szyfrowania/deszyfrowania"""
    
    def __init__(self):
        super().__init__()
        self.key = None
        app_logger.log_app_start()
        self.init_ui()
        self.setup_styles()
        
    def init_ui(self):
        """Inicjalizacja interfejsu użytkownika"""
        self.setWindowTitle("Aplikacja Szyfrowania/Deszyfrowania")
        self.setGeometry(100, 100, 800, 600)
        self.setMinimumSize(600, 400)
        self.showMaximized()
        
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
        app_logger.log_user_action("wybrano szyfrowanie")
        app_logger.log_window_open("ChoiceWindow (szyfrowanie)")
        from views.choice_window import ChoiceWindow
        self.choice_window = ChoiceWindow(self, "encrypt")
        self.choice_window.show()
        
    def show_decrypt_window(self):
        """Pokazuje okno wyboru deszyfrowania"""
        app_logger.log_user_action("wybrano deszyfrowanie")
        app_logger.log_window_open("ChoiceWindow (deszyfrowanie)")
        from views.choice_window import ChoiceWindow
        self.choice_window = ChoiceWindow(self, "decrypt")
        self.choice_window.show()




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
