#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Okno deszyfrowania tekstu zaszyfrowanego metodą podwójnej transpozycji kolumnowej.
"""

from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QTextEdit,
    QLineEdit,
    QPushButton,
    QMessageBox,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from utils.double_transposition_cipher import double_transposition_decrypt_text
from utils.logger import app_logger


class DecryptTextDoubleTranspositionWindow(QMainWindow):
    """UI do deszyfrowania tekstu (hex) metodą podwójnej transpozycji."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        app_logger.log_window_open("DecryptTextDoubleTranspositionWindow")
        self._init_ui()
        self._apply_styles()

    def _init_ui(self):
        self.setWindowTitle("Deszyfrowanie – Podwójna transpozycja")
        self.setGeometry(160, 160, 900, 600)
        self.showMaximized()

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(18)
        layout.setContentsMargins(30, 30, 30, 30)

        title = QLabel("🧩 Podwójna transpozycja kolumnowa – deszyfrowanie tekstu")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setStyleSheet(
            "background: white; border-radius: 12px; padding: 16px; color: #1d3557;"
        )
        layout.addWidget(title)

        layout.addWidget(self._build_label("Zaszyfrowany tekst (hex):"))
        self.cipher_edit = QTextEdit()
        self.cipher_edit.setPlaceholderText("Wklej dane hex wygenerowane przez ten sam moduł…")
        self.cipher_edit.setMinimumHeight(150)
        layout.addWidget(self.cipher_edit)

        keys = QHBoxLayout()
        keys.setSpacing(12)
        self.key_a = self._build_key_field("Klucz A (jak przy szyfrowaniu)")
        self.key_b = self._build_key_field("Klucz B (jak przy szyfrowaniu)")
        keys.addWidget(self.key_a)
        keys.addWidget(self.key_b)
        layout.addLayout(keys)

        buttons = QHBoxLayout()
        self.decrypt_btn = QPushButton("🔓 Deszyfruj")
        self.decrypt_btn.clicked.connect(self.decrypt_text)
        buttons.addWidget(self.decrypt_btn)

        self.clear_btn = QPushButton("🗑️ Wyczyść")
        self.clear_btn.clicked.connect(self.clear_fields)
        buttons.addWidget(self.clear_btn)
        buttons.addStretch()
        layout.addLayout(buttons)

        layout.addWidget(self._build_label("Tekst jawny:"))
        self.result_edit = QTextEdit()
        self.result_edit.setReadOnly(True)
        self.result_edit.setMinimumHeight(140)
        layout.addWidget(self.result_edit)

        self.back_btn = QPushButton("⬅️ Powrót")
        self.back_btn.clicked.connect(self.go_back)
        layout.addWidget(self.back_btn, alignment=Qt.AlignRight)

    def _apply_styles(self):
        self.setStyleSheet(
            """
            QMainWindow { background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #fef6fb, stop:1 #e3f2fd); }
            QTextEdit, QLineEdit {
                border: 2px solid #d4c4fb;
                border-radius: 10px;
                padding: 10px;
                background: white;
                font-size: 14px;
            }
            QPushButton {
                border-radius: 10px;
                padding: 12px 18px;
                background: #ff6b6b;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover { background: #ef4444; }
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

    def decrypt_text(self):
        cipher_hex = self.cipher_edit.toPlainText().strip()
        key_a = self.key_a.text()
        key_b = self.key_b.text()

        if not cipher_hex:
            QMessageBox.warning(self, "Brak danych", "Wklej zaszyfrowany tekst (hex).")
            return

        try:
            plaintext = double_transposition_decrypt_text(cipher_hex, key_a, key_b)
            self.result_edit.setPlainText(plaintext)
            QMessageBox.information(
                self, "Sukces", "Tekst został odszyfrowany metodą podwójnej transpozycji."
            )
            from views.log_window_helper import show_log_window

            show_log_window(self)
        except ValueError as exc:
            QMessageBox.warning(self, "Nieprawidłowe dane", str(exc))
        except Exception as exc:  # noqa: BLE001
            app_logger.log_error("double transposition decrypt text", str(exc))
            QMessageBox.critical(self, "Błąd", f"Nie udało się odszyfrować: {exc}")

    def clear_fields(self):
        self.cipher_edit.clear()
        self.result_edit.clear()

    def go_back(self):
        if self.parent:
            self.parent.show()
        self.close()


