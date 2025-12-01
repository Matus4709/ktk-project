#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Okno szyfrowania tekstu szyfrem podwójnej transpozycji kolumnowej.
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
    QApplication,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from utils.double_transposition_cipher import double_transposition_encrypt_text
from utils.logger import app_logger


class EncryptTextDoubleTranspositionWindow(QMainWindow):
    """UI do szyfrowania tekstu metodą podwójnej transpozycji kolumnowej."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        app_logger.log_window_open("EncryptTextDoubleTranspositionWindow")
        self._init_ui()
        self._apply_styles()

    def _init_ui(self):
        self.setWindowTitle("Szyfrowanie – Podwójna transpozycja")
        self.setGeometry(160, 160, 900, 600)
        self.showMaximized()

        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)
        layout.setSpacing(18)
        layout.setContentsMargins(30, 30, 30, 30)

        title = QLabel("🧩 Podwójna transpozycja kolumnowa – szyfrowanie tekstu")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setStyleSheet(
            "background: white; border-radius: 12px; padding: 16px; color: #1d3557;"
        )
        layout.addWidget(title)

        layout.addWidget(self._build_label("Tekst jawny:"))
        self.plain_edit = QTextEdit()
        self.plain_edit.setPlaceholderText("Wklej tekst do zaszyfrowania…")
        self.plain_edit.setMinimumHeight(150)
        layout.addWidget(self.plain_edit)

        key_layout = QHBoxLayout()
        key_layout.setSpacing(12)
        self.key_a = self._build_key_field("Klucz A (kolejność kolumn)")
        self.key_b = self._build_key_field("Klucz B (druga permutacja)")
        key_layout.addWidget(self.key_a)
        key_layout.addWidget(self.key_b)
        layout.addLayout(key_layout)

        buttons = QHBoxLayout()
        self.encrypt_btn = QPushButton("🔒 Szyfruj")
        self.encrypt_btn.clicked.connect(self.encrypt_text)
        buttons.addWidget(self.encrypt_btn)

        self.clear_btn = QPushButton("🗑️ Wyczyść")
        self.clear_btn.clicked.connect(self.clear_fields)
        buttons.addWidget(self.clear_btn)

        buttons.addStretch()
        layout.addLayout(buttons)

        layout.addWidget(self._build_label("Wynik (hex):"))
        self.result_edit = QTextEdit()
        self.result_edit.setReadOnly(True)
        self.result_edit.setMinimumHeight(140)
        layout.addWidget(self.result_edit)

        self.copy_btn = QPushButton("📋 Kopiuj wynik")
        self.copy_btn.clicked.connect(self.copy_result)
        layout.addWidget(self.copy_btn)

        self.back_btn = QPushButton("⬅️ Powrót")
        self.back_btn.clicked.connect(self.go_back)
        layout.addWidget(self.back_btn, alignment=Qt.AlignRight)

    def _apply_styles(self):
        self.setStyleSheet(
            """
            QMainWindow { background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #edf2fb, stop:1 #d7e3fc); }
            QTextEdit, QLineEdit {
                border: 2px solid #bcccdc;
                border-radius: 10px;
                padding: 10px;
                background: white;
                font-size: 14px;
            }
            QPushButton {
                border-radius: 10px;
                padding: 12px 18px;
                background: #3a86ff;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover { background: #2563eb; }
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

    def encrypt_text(self):
        plaintext = self.plain_edit.toPlainText()
        key_a = self.key_a.text()
        key_b = self.key_b.text()

        if not plaintext.strip():
            QMessageBox.warning(self, "Brak danych", "Wprowadź tekst do zaszyfrowania.")
            return

        try:
            cipher_hex = double_transposition_encrypt_text(plaintext, key_a, key_b)
            self.result_edit.setPlainText(cipher_hex)
            QMessageBox.information(
                self, "Sukces", "Tekst został zaszyfrowany metodą podwójnej transpozycji."
            )
            from views.log_window_helper import show_log_window

            show_log_window(self)
        except ValueError as exc:
            QMessageBox.warning(self, "Nieprawidłowy klucz", str(exc))
        except Exception as exc:  # noqa: BLE001
            app_logger.log_error("double transposition encrypt text", str(exc))
            QMessageBox.critical(self, "Błąd", f"Nie udało się zaszyfrować: {exc}")

    def clear_fields(self):
        self.plain_edit.clear()
        self.result_edit.clear()

    def copy_result(self):
        text = self.result_edit.toPlainText()
        if not text:
            QMessageBox.warning(self, "Brak danych", "Brak wyniku do skopiowania.")
            return
        QApplication.clipboard().setText(text)
        QMessageBox.information(self, "Skopiowano", "Wynik skopiowano do schowka.")

    def go_back(self):
        if self.parent:
            self.parent.show()
        self.close()


