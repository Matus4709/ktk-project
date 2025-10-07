#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Okno szyfrowania pliku
"""

import os
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QLineEdit, QFileDialog, 
                             QMessageBox, QApplication, QTextEdit, QComboBox,
                             QGroupBox, QGridLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from utils.caesar_cipher import caesar_encrypt_file
from utils.logger import app_logger


class EncryptFileWindow(QMainWindow):
    """Okno szyfrowania pliku"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        app_logger.log_window_open("EncryptFileWindow")
        self.init_ui()
        self.setup_styles()
        
    def init_ui(self):
        """Inicjalizacja interfejsu okna szyfrowania pliku"""
        self.setWindowTitle("Szyfrowanie Pliku")
        self.setGeometry(200, 200, 700, 600)
        self.setMinimumSize(600, 500)
        self.showMaximized()
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
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
        
        # Sekcja wyboru pliku
        file_group = QGroupBox("📁 Wybór pliku")
        file_group.setFont(QFont("Arial", 12, QFont.Bold))
        file_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #bdc3c7;
                border-radius: 10px;
                margin-top: 10px;
                padding-top: 10px;
                background: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        file_layout = QVBoxLayout(file_group)
        file_layout.setSpacing(10)
        
        file_label = QLabel("Plik do szyfrowania:")
        file_label.setFont(QFont("Arial", 11, QFont.Bold))
        file_layout.addWidget(file_label)
        
        file_input_layout = QHBoxLayout()
        
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
        file_input_layout.addWidget(self.file_input)
        
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
        file_input_layout.addWidget(self.browse_btn)
        
        file_layout.addLayout(file_input_layout)
        layout.addWidget(file_group)
        
        # Sekcja opcji szyfru Cezara
        cipher_group = QGroupBox("🔤 Opcje szyfru Cezara")
        cipher_group.setFont(QFont("Arial", 12, QFont.Bold))
        cipher_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #bdc3c7;
                border-radius: 10px;
                margin-top: 10px;
                padding-top: 10px;
                background: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        cipher_layout = QVBoxLayout(cipher_group)
        cipher_layout.setSpacing(10)
        
        shift_label = QLabel("Przesunięcie (1-25):")
        shift_label.setFont(QFont("Arial", 11, QFont.Bold))
        cipher_layout.addWidget(shift_label)
        
        shift_layout = QHBoxLayout()
        self.shift_input = QLineEdit()
        self.shift_input.setPlaceholderText("Wprowadź przesunięcie (1-25)")
        self.shift_input.setText("3")
        self.shift_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                padding: 8px;
                font-size: 11px;
                background: white;
                max-width: 150px;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
        """)
        shift_layout.addWidget(self.shift_input)
        shift_layout.addStretch()
        cipher_layout.addLayout(shift_layout)
        
        layout.addWidget(cipher_group)
        
        # Przyciski
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)
        
        self.preview_btn = QPushButton("👁️ Podgląd")
        self.preview_btn.setMinimumSize(120, 40)
        self.preview_btn.setFont(QFont("Arial", 12, QFont.Bold))
        self.preview_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #f39c12, stop:1 #e67e22);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #e67e22, stop:1 #d35400);
            }
        """)
        self.preview_btn.clicked.connect(self.preview_encryption)
        buttons_layout.addWidget(self.preview_btn)
        
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
        
        # Sekcja wyników
        result_group = QGroupBox("📊 Wynik")
        result_group.setFont(QFont("Arial", 12, QFont.Bold))
        result_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #bdc3c7;
                border-radius: 10px;
                margin-top: 10px;
                padding-top: 10px;
                background: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        result_layout = QVBoxLayout(result_group)
        result_layout.setSpacing(10)
        
        result_label = QLabel("Informacje o szyfrowaniu:")
        result_label.setFont(QFont("Arial", 11, QFont.Bold))
        result_layout.addWidget(result_label)
        
        self.result_output = QTextEdit()
        self.result_output.setReadOnly(True)
        self.result_output.setMinimumHeight(200)
        self.result_output.setMaximumHeight(300)
        self.result_output.setStyleSheet("""
            QTextEdit {
                border: 2px solid #27ae60;
                border-radius: 8px;
                padding: 15px;
                font-size: 12px;
                background: #f8f9fa;
                line-height: 1.4;
            }
        """)
        result_layout.addWidget(self.result_output)
        
        layout.addWidget(result_group)
        
        # Przycisk powrotu
        back_layout = QHBoxLayout()
        back_layout.addStretch()
        
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
        
        layout.addLayout(back_layout)
        
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
            
    def preview_encryption(self):
        """Pokazuje podgląd szyfrowania pliku"""
        file_path = self.file_input.text().strip()
        if not file_path:
            app_logger.log_validation_error("plik", "nie wybrano pliku")
            QMessageBox.warning(self, "Błąd", "Wybierz plik do szyfrowania!")
            return
            
        if not os.path.exists(file_path):
            app_logger.log_validation_error("plik", f"plik nie istnieje: {file_path}")
            QMessageBox.warning(self, "Błąd", "Wybrany plik nie istnieje!")
            return
            
        try:
            shift = int(self.shift_input.text().strip())
            if shift < 1 or shift > 25:
                app_logger.log_validation_error("przesunięcie", f"poza zakresem: {shift}")
                QMessageBox.warning(self, "Błąd", "Przesunięcie musi być liczbą od 1 do 25!")
                return
                
            app_logger.log_preview("szyfrowania", file_path, shift)
            
            # Wczytaj początek pliku do podglądu
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Ogranicz do pierwszych 500 znaków dla podglądu
            preview_content = content[:500]
            if len(content) > 500:
                preview_content += "\n... (plik jest dłuższy)"
            
            # Zaszyfruj podgląd
            from utils.caesar_cipher import caesar_encrypt
            encrypted_preview = caesar_encrypt(preview_content, shift)
            
            # Wyświetl podgląd
            self.result_output.setPlainText(
                f"👁️ PODGLĄD SZYFROWANIA PLIKU\n\n"
                f"📁 Plik: {os.path.basename(file_path)}\n"
                f"🔢 Przesunięcie: {shift}\n"
                f"📏 Rozmiar pliku: {len(content)} znaków\n\n"
                f"📝 Oryginalny tekst (pierwsze 500 znaków):\n"
                f"{preview_content}\n\n"
                f"🔒 Zaszyfrowany tekst:\n"
                f"{encrypted_preview}\n\n"
                f"💡 Kliknij 'Szyfruj plik' aby zapisać pełny zaszyfrowany plik"
            )
            
        except ValueError:
            app_logger.log_validation_error("przesunięcie", "nieprawidłowy format")
            QMessageBox.warning(self, "Błąd", "Przesunięcie musi być liczbą całkowitą!")
        except Exception as e:
            app_logger.log_error("podgląd szyfrowania", str(e))
            QMessageBox.critical(self, "Błąd", f"Wystąpił błąd podczas podglądu: {str(e)}")
            
    def encrypt_file(self):
        """Szyfruje plik szyfrem Cezara"""
        file_path = self.file_input.text().strip()
        if not file_path:
            app_logger.log_validation_error("plik", "nie wybrano pliku")
            QMessageBox.warning(self, "Błąd", "Wybierz plik do szyfrowania!")
            return
            
        if not os.path.exists(file_path):
            app_logger.log_validation_error("plik", f"plik nie istnieje: {file_path}")
            QMessageBox.warning(self, "Błąd", "Wybrany plik nie istnieje!")
            return
            
        try:
            shift = int(self.shift_input.text().strip())
            if shift < 1 or shift > 25:
                app_logger.log_validation_error("przesunięcie", f"poza zakresem: {shift}")
                QMessageBox.warning(self, "Błąd", "Przesunięcie musi być liczbą od 1 do 25!")
                return
                
            # Wybierz lokalizację zapisu
            output_path, _ = QFileDialog.getSaveFileName(
                self, 
                "Zapisz zaszyfrowany plik jako", 
                file_path + ".encrypted", 
                "Wszystkie pliki (*.*)"
            )
            
            if not output_path:
                app_logger.log_user_action("anulowano wybór lokalizacji zapisu")
                return
                
            app_logger.log_file_operation("Szyfrowanie", file_path, shift)
            success = caesar_encrypt_file(file_path, output_path, shift)
            
            if success:
                app_logger.log_file_success("Szyfrowanie", file_path, output_path)
                self.result_output.setPlainText(
                    f"🔒 SZYFROWANIE PLIKU ZAKOŃCZONE SUKCESEM!\n\n"
                    f"📁 Oryginalny plik: {os.path.basename(file_path)}\n"
                    f"🔐 Zaszyfrowany plik: {os.path.basename(output_path)}\n"
                    f"🔢 Przesunięcie: {shift}\n"
                    f"📍 Lokalizacja: {output_path}"
                )
                QMessageBox.information(self, "Sukces", 
                    f"Plik został zaszyfrowany szyfrem Cezara z przesunięciem {shift}!\n"
                    f"Zapisano jako: {os.path.basename(output_path)}")
            else:
                app_logger.log_error("szyfrowanie pliku", "nie udało się zaszyfrować pliku")
                QMessageBox.critical(self, "Błąd", "Wystąpił błąd podczas szyfrowania pliku!")
                
        except ValueError:
            app_logger.log_validation_error("przesunięcie", "nieprawidłowy format")
            QMessageBox.warning(self, "Błąd", "Przesunięcie musi być liczbą całkowitą!")
        except Exception as e:
            app_logger.log_error("szyfrowanie pliku", str(e))
            QMessageBox.critical(self, "Błąd", f"Wystąpił błąd podczas szyfrowania: {str(e)}")
            
    def clear_fields(self):
        """Czyści wszystkie pola"""
        self.file_input.clear()
        self.shift_input.setText("3")
        self.result_output.clear()
        
    def go_back(self):
        """Powrót do okna wyboru"""
        if self.parent:
            self.parent.show()
        self.close()
