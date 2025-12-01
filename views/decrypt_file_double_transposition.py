#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Okno deszyfrowania plików zaszyfrowanych metodą podwójnej transpozycji kolumnowej.
"""

import os

from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QFileDialog,
    QTextEdit,
    QMessageBox,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from utils.double_transposition_cipher import double_transposition_decrypt_file
from utils.logger import app_logger


class DecryptFileDoubleTranspositionWindow(QMainWindow):
    """UI do deszyfrowania plików zaszyfrowanych nowym szyfrem."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        app_logger.log_window_open("DecryptFileDoubleTranspositionWindow")
        self._init_ui()
        self._apply_styles()

    def _init_ui(self):
        self.setWindowTitle("Deszyfrowanie pliku – Podwójna transpozycja")
        self.setGeometry(200, 200, 860, 520)
        self.showMaximized()

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(18)
        layout.setContentsMargins(30, 30, 30, 30)

        title = QLabel("🧩 Podwójna transpozycja kolumnowa – deszyfrowanie pliku")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setStyleSheet(
            "background: white; border-radius: 12px; padding: 16px; color: #0f172a;"
        )
        layout.addWidget(title)

        layout.addWidget(self._build_label("Zaszyfrowany plik:"))
        file_row = QHBoxLayout()
        self.file_input = QLineEdit()
        self.file_input.setPlaceholderText("Wskaż plik .dtc do odszyfrowania…")
        self.file_input.setReadOnly(True)
        file_row.addWidget(self.file_input)

        browse_btn = QPushButton("📁 Przeglądaj")
        browse_btn.clicked.connect(self.choose_file)
        file_row.addWidget(browse_btn)
        layout.addLayout(file_row)

        keys_row = QHBoxLayout()
        keys_row.setSpacing(12)
        self.key_a = self._build_key_field("Klucz A")
        self.key_b = self._build_key_field("Klucz B")
        keys_row.addWidget(self.key_a)
        keys_row.addWidget(self.key_b)
        layout.addLayout(keys_row)

        buttons = QHBoxLayout()
        decrypt_btn = QPushButton("🔓 Deszyfruj plik")
        decrypt_btn.clicked.connect(self.decrypt_file)
        buttons.addWidget(decrypt_btn)

        clear_btn = QPushButton("🗑️ Wyczyść")
        clear_btn.clicked.connect(self.clear_fields)
        buttons.addWidget(clear_btn)
        buttons.addStretch()
        layout.addLayout(buttons)

        layout.addWidget(self._build_label("Log operacji:"))
        self.log_view = QTextEdit()
        self.log_view.setReadOnly(True)
        self.log_view.setMinimumHeight(200)
        layout.addWidget(self.log_view)

        self.back_btn = QPushButton("⬅️ Powrót")
        self.back_btn.clicked.connect(self.go_back)
        layout.addWidget(self.back_btn, alignment=Qt.AlignRight)

    def _apply_styles(self):
        self.setStyleSheet(
            """
            QMainWindow { background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #fdf2f8, stop:1 #e0f2fe); }
            QLineEdit {
                border: 2px solid #c4b5fd;
                border-radius: 10px;
                padding: 10px;
                background: white;
                font-size: 14px;
            }
            QTextEdit {
                border: 2px solid #c4b5fd;
                border-radius: 10px;
                padding: 12px;
                background: white;
                font-family: 'Courier New', monospace;
            }
            QPushButton {
                border-radius: 10px;
                padding: 12px 18px;
                background: #ec4899;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover { background: #db2777; }
            """
        )

    def _build_label(self, text: str) -> QLabel:
        lbl = QLabel(text)
        lbl.setFont(QFont("Arial", 12, QFont.Bold))
        return lbl

    def _build_key_field(self, placeholder: str) -> QLineEdit:
        field = QLineEdit()
        field.setPlaceholderText(placeholder)
        field.setMaxLength(64)
        return field

    def choose_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Wybierz zaszyfrowany plik", filter="Pliki zaszyfrowane (*.dtc);;Wszystkie (*.*)"
        )
        if path:
            self.file_input.setText(path)

    def decrypt_file(self):
        input_path = self.file_input.text().strip()
        if not input_path or not os.path.exists(input_path):
            QMessageBox.warning(self, "Brak pliku", "Wskaż istniejący zaszyfrowany plik.")
            return

        key_a = self.key_a.text()
        key_b = self.key_b.text()

        output_path, _ = QFileDialog.getSaveFileName(
            self,
            "Zapisz odszyfrowany plik jako",
            os.path.splitext(input_path)[0] + "_decrypted",
            "Wszystkie pliki (*.*)",
        )
        if not output_path:
            return

        self.log_view.append(f"▶️ Deszyfrowanie: {os.path.basename(input_path)}")
        success = double_transposition_decrypt_file(input_path, output_path, key_a, key_b)
        if success:
            self.log_view.append(f"✅ Odszyfrowano do: {output_path}\n")
            QMessageBox.information(
                self, "Sukces", f"Plik odszyfrowano i zapisano jako:\n{output_path}"
            )
        else:
            self.log_view.append("❌ Operacja nie powiodła się.\n")
            QMessageBox.critical(
                self, "Błąd", "Nie udało się odszyfrować pliku. Sprawdź logi."
            )

    def clear_fields(self):
        self.file_input.clear()
        self.key_a.clear()
        self.key_b.clear()
        self.log_view.clear()

    def go_back(self):
        if self.parent:
            self.parent.show()
        self.close()


