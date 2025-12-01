"""
Okno wizualizujące wymianę kluczy ECDH z możliwością zapisu/wczytywania kluczy.
"""

from __future__ import annotations

from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QComboBox,
    QTextEdit,
    QMessageBox,
    QFrame,
    QSpinBox,
    QApplication,
    QFileDialog,
    QGridLayout,
    QScrollArea,
    QGraphicsDropShadowEffect,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor

from utils.ecdh import (
    ecdh_generate_key_pair,
    ecdh_compute_shared_secret,
)
from utils.logger import app_logger


class ECDHWindow(QMainWindow):
    """Interfejs użytkownika do demonstracji ECDH."""

    CURVE_OPTIONS = [
        ("SECP256R1", "secp256r1 (prime256v1) – ~128 bitów bezpieczeństwa"),
        ("SECP384R1", "secp384r1 – ~192 bity bezpieczeństwa"),
        ("SECP521R1", "secp521r1 – ~256 bitów bezpieczeństwa"),
        ("SECP256K1", "secp256k1 (Bitcoin)"),
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()
        app_logger.log_window_open("ECDHWindow")

    def init_ui(self):
        self.setWindowTitle("🤝 ECDH – wymiana kluczy")
        self.setGeometry(200, 200, 1100, 780)
        self.setMinimumSize(900, 640)
        self.showMaximized()

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        root_layout = QVBoxLayout(main_widget)
        root_layout.setContentsMargins(30, 30, 30, 30)
        root_layout.setSpacing(0)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        root_layout.addWidget(scroll_area)

        scroll_host = QWidget()
        scroll_area.setWidget(scroll_host)

        host_layout = QHBoxLayout(scroll_host)
        host_layout.setContentsMargins(0, 0, 0, 0)
        host_layout.addStretch()

        content_widget = QWidget()
        content_widget.setObjectName("content_widget")
        content_widget.setMinimumWidth(960)
        content_widget.setMaximumWidth(1200)
        content_widget.setStyleSheet(
            """
            QWidget#content_widget {
                background-color: rgba(255, 255, 255, 0.94);
                border-radius: 28px;
                padding: 36px;
            }
            """
        )
        host_layout.addWidget(content_widget)
        host_layout.addStretch()

        main_layout = QVBoxLayout(content_widget)
        main_layout.setSpacing(30)
        main_layout.setAlignment(Qt.AlignTop)

        hero = QFrame()
        hero.setObjectName("heroCard")
        hero_layout = QVBoxLayout(hero)
        hero_layout.setSpacing(10)
        hero.setStyleSheet(
            """
            QFrame#heroCard {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #ffffff, stop:1 #f5f8fb);
                border-radius: 24px;
                border: 1px solid #e4ebf3;
                padding: 22px;
            }
            """
        )

        title = QLabel("🤝 Elliptic Curve Diffie-Hellman (ECDH)")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Inter", 28, QFont.Bold))
        title.setStyleSheet("color: #1d3557;")
        hero_layout.addWidget(title)

        description = QLabel(
            "Generuj parę kluczy eliptycznych, udostępnij klucz publiczny partnerowi "
            "i oblicz wspólny sekret zabezpieczony HKDF."
        )
        description.setAlignment(Qt.AlignCenter)
        description.setWordWrap(True)
        description.setStyleSheet("color: #607287; font-size: 15px;")
        hero_layout.addWidget(description)

        badge_row = QHBoxLayout()
        badge_row.setSpacing(12)
        badge_row.setAlignment(Qt.AlignCenter)
        for text in ("✅ 3 kroki", "🔐 256-bit security", "⚙️ HKDF ready"):
            pill = QLabel(text)
            pill.setStyleSheet(
                """
                QLabel {
                    background-color: #ecf3ff;
                    color: #2c5eff;
                    border-radius: 14px;
                    padding: 6px 14px;
                    font-weight: 600;
                }
                """
            )
            badge_row.addWidget(pill)
        hero_layout.addLayout(badge_row)
        main_layout.addWidget(hero)

        selection_frame = QFrame()
        selection_frame.setFrameStyle(QFrame.StyledPanel)
        selection_frame.setStyleSheet(
            """
            QFrame {
                background-color: #f7f9fb;
                border: 2px solid #dfe6ec;
                border-radius: 16px;
                padding: 18px 24px;
            }
            """
        )
        self._apply_card_shadow(selection_frame)
        selection_layout = QHBoxLayout(selection_frame)
        selection_layout.setSpacing(15)

        curve_label = QLabel("🔁 Krzywa eliptyczna:")
        curve_label.setFont(QFont("Inter", 13, QFont.DemiBold))
        selection_layout.addWidget(curve_label)

        self.curve_combo = QComboBox()
        for name, text in self.CURVE_OPTIONS:
            self.curve_combo.addItem(text, userData=name)
        self.curve_combo.setCurrentIndex(0)
        self.curve_combo.setStyleSheet(
            """
            QComboBox {
                border: 2px solid #dee2e6;
                border-radius: 12px;
                padding: 10px;
                background-color: white;
                min-width: 260px;
                font-size: 14px;
            }
            QComboBox::drop-down {
                width: 28px;
            }
            """
        )
        selection_layout.addWidget(self.curve_combo)
        selection_layout.addStretch()
        main_layout.addWidget(selection_frame)

        keys_frame = self._build_keys_frame()
        self._apply_card_shadow(keys_frame)
        main_layout.addWidget(keys_frame)

        exchange_frame = self._build_exchange_frame()
        self._apply_card_shadow(exchange_frame)
        main_layout.addWidget(exchange_frame)

        buttons_layout = QHBoxLayout()
        buttons_layout.setContentsMargins(0, 10, 0, 0)

        self.log_button = QPushButton("📜 Pokaż logi")
        self.log_button.clicked.connect(self.show_log_window)
        self._style_primary_button(self.log_button, "#17a2b8")
        buttons_layout.addWidget(self.log_button)

        buttons_layout.addStretch()

        self.back_button = QPushButton("⬅️ Powrót")
        self._style_primary_button(self.back_button, "#28a745")
        self.back_button.clicked.connect(self.go_back)
        buttons_layout.addWidget(self.back_button)

        main_layout.addLayout(buttons_layout)

        self.setStyleSheet(
            """
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #dfe9f3, stop:1 #ffffff);
            }
            """
        )

    def _build_keys_frame(self) -> QFrame:
        frame = QFrame()
        frame.setFrameStyle(QFrame.StyledPanel)
        frame.setStyleSheet(
            """
            QFrame {
                background-color: #ffffff;
                border: 2px solid #dfe6ec;
                border-radius: 20px;
                padding: 24px;
            }
            """
        )
        layout = QVBoxLayout(frame)
        layout.setSpacing(18)

        header = QLabel("1️⃣ Generowanie pary kluczy")
        header.setFont(QFont("Inter", 16, QFont.Bold))
        header.setStyleSheet("color: #2c3e50;")
        layout.addWidget(header)

        info = QLabel(
            "Klucz prywatny trzymaj w sekrecie, klucz publiczny możesz udostępnić partnerowi."
        )
        info.setStyleSheet("color: #7f8c8d;")
        info.setWordWrap(True)
        layout.addWidget(info)

        self.private_key_edit = QTextEdit()
        self.private_key_edit.setPlaceholderText("Klucz prywatny (PEM)")
        self._style_text_area(self.private_key_edit)

        self.public_key_edit = QTextEdit()
        self.public_key_edit.setPlaceholderText("Klucz publiczny (PEM)")
        self.public_key_edit.setReadOnly(True)
        self._style_text_area(self.public_key_edit)

        grid = QGridLayout()
        grid.setSpacing(12)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)
        grid.addWidget(QLabel("🔒 Klucz prywatny:"), 0, 0)
        grid.addWidget(QLabel("📤 Klucz publiczny:"), 0, 1)
        grid.addWidget(self.private_key_edit, 1, 0)
        grid.addWidget(self.public_key_edit, 1, 1)
        layout.addLayout(grid)

        private_actions = QHBoxLayout()
        private_actions.addWidget(
            self._build_secondary_button(
                "📂 Wczytaj",
                lambda: self.load_key_from_file(
                    "Wczytaj klucz prywatny", self.private_key_edit
                ),
            )
        )
        private_actions.addWidget(
            self._build_secondary_button(
                "💾 Zapisz",
                lambda: self.save_key_to_file(
                    "Zapisz klucz prywatny",
                    "private_key.pem",
                    self.private_key_edit.toPlainText(),
                ),
            )
        )
        private_actions.addStretch()
        grid.addLayout(private_actions, 2, 0)

        public_actions = QHBoxLayout()
        public_actions.addWidget(
            self._build_secondary_button(
                "📂 Wczytaj",
                lambda: self.load_key_from_file(
                    "Wczytaj klucz publiczny", self.public_key_edit
                ),
            )
        )
        public_actions.addWidget(
            self._build_secondary_button(
                "💾 Zapisz",
                lambda: self.save_key_to_file(
                    "Zapisz klucz publiczny",
                    "public_key.pem",
                    self.public_key_edit.toPlainText(),
                ),
            )
        )
        public_actions.addStretch()
        grid.addLayout(public_actions, 2, 1)

        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(12)

        self.generate_button = QPushButton("⚙️ Generuj parę kluczy")
        self._style_primary_button(self.generate_button, "#007bff")
        self.generate_button.clicked.connect(self.generate_keys)
        buttons_layout.addWidget(self.generate_button)

        self.copy_public_button = QPushButton("📋 Kopiuj klucz publiczny")
        self._style_primary_button(self.copy_public_button, "#6c757d")
        self.copy_public_button.clicked.connect(
            lambda: self.copy_text(self.public_key_edit.toPlainText())
        )
        buttons_layout.addWidget(self.copy_public_button)
        buttons_layout.addStretch()
        layout.addLayout(buttons_layout)
        return frame

    def _build_exchange_frame(self) -> QFrame:
        frame = QFrame()
        frame.setFrameStyle(QFrame.StyledPanel)
        frame.setStyleSheet(
            """
            QFrame {
                background-color: #ffffff;
                border: 2px solid #dfe6ec;
                border-radius: 20px;
                padding: 24px;
            }
            """
        )
        layout = QVBoxLayout(frame)
        layout.setSpacing(18)

        header = QLabel("2️⃣ Oblicz wspólny sekret")
        header.setFont(QFont("Inter", 16, QFont.Bold))
        header.setStyleSheet("color: #2c3e50;")
        layout.addWidget(header)

        peer_label = QLabel("📨 Klucz publiczny partnera (PEM):")
        layout.addWidget(peer_label)

        self.peer_public_edit = QTextEdit()
        self.peer_public_edit.setPlaceholderText("Wklej otrzymany klucz publiczny partnera...")
        self._style_text_area(self.peer_public_edit)
        layout.addWidget(self.peer_public_edit)

        peer_actions = QHBoxLayout()
        peer_actions.addWidget(
            self._build_secondary_button(
                "📂 Wczytaj od partnera",
                lambda: self.load_key_from_file(
                    "Wczytaj klucz partnera", self.peer_public_edit
                ),
            )
        )
        peer_actions.addWidget(
            self._build_secondary_button(
                "💾 Zapisz klucz partnera",
                lambda: self.save_key_to_file(
                    "Zapisz klucz partnera",
                    "peer_public_key.pem",
                    self.peer_public_edit.toPlainText(),
                ),
            )
        )
        peer_actions.addStretch()
        layout.addLayout(peer_actions)

        hkdf_layout = QHBoxLayout()
        hkdf_label = QLabel("🔑 Długość klucza HKDF (bajty):")
        hkdf_layout.addWidget(hkdf_label)
        self.hkdf_length_spin = QSpinBox()
        self.hkdf_length_spin.setRange(16, 64)
        self.hkdf_length_spin.setValue(32)
        hkdf_layout.addWidget(self.hkdf_length_spin)
        hkdf_layout.addStretch()
        layout.addLayout(hkdf_layout)

        self.shared_secret_edit = QTextEdit()
        self.shared_secret_edit.setPlaceholderText("Surowy sekret ECDH (hex)")
        self.shared_secret_edit.setReadOnly(True)
        self._style_text_area(self.shared_secret_edit)

        self.derived_key_edit = QTextEdit()
        self.derived_key_edit.setPlaceholderText("Klucz po HKDF (hex)")
        self.derived_key_edit.setReadOnly(True)
        self._style_text_area(self.derived_key_edit)

        layout.addWidget(QLabel("🧮 Surowy sekret:"))
        layout.addWidget(self.shared_secret_edit)
        layout.addWidget(QLabel("🔐 Klucz symetryczny (HKDF):"))
        layout.addWidget(self.derived_key_edit)

        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(12)

        self.exchange_button = QPushButton("🤝 Oblicz wspólny sekret")
        self._style_primary_button(self.exchange_button, "#e67e22")
        self.exchange_button.clicked.connect(self.compute_secret)
        buttons_layout.addWidget(self.exchange_button)

        self.copy_secret_button = QPushButton("📋 Kopiuj klucz HKDF")
        self._style_primary_button(self.copy_secret_button, "#6c757d")
        self.copy_secret_button.clicked.connect(
            lambda: self.copy_text(self.derived_key_edit.toPlainText())
        )
        buttons_layout.addWidget(self.copy_secret_button)
        buttons_layout.addStretch()
        layout.addLayout(buttons_layout)
        return frame

    def _style_text_area(self, widget: QTextEdit):
        widget.setMinimumHeight(140)
        widget.setStyleSheet(
            """
            QTextEdit {
                border: 2px solid #dee2e6;
                border-radius: 12px;
                padding: 12px;
                font-family: 'JetBrains Mono', 'Courier New', monospace;
                background-color: #fafafa;
            }
            QTextEdit:focus {
                border-color: #007bff;
                background-color: #ffffff;
            }
            """
        )

    def _style_primary_button(self, button: QPushButton, color: str):
        button.setStyleSheet(
            f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {color}, stop:1 {color});
                color: white;
                border: none;
                border-radius: 14px;
                padding: 14px 20px;
                font-size: 15px;
                font-weight: bold;
                letter-spacing: 0.3px;
            }}
            QPushButton:hover {{
                opacity: 0.88;
            }}
            QPushButton:disabled {{
                background: #95a5a6;
            }}
            """
        )
        button.setMinimumHeight(48)

    def _build_secondary_button(self, text: str, callback):
        """Utility that returns a subtle action button."""
        button = QPushButton(text)
        button.clicked.connect(callback)
        button.setStyleSheet(
            """
            QPushButton {
                background-color: #f0f3f6;
                color: #2c3e50;
                border: 1px solid #d5dee6;
                border-radius: 10px;
                padding: 9px 14px;
            }
            QPushButton:hover {
                background-color: #e2e8ef;
            }
            """
        )
        return button

    def _apply_card_shadow(self, widget: QWidget):
        """Adds a subtle drop shadow to card-like widgets."""
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(28)
        shadow.setColor(QColor(0, 0, 0, 35))
        shadow.setOffset(0, 10)
        widget.setGraphicsEffect(shadow)

    def selected_curve(self) -> str:
        return self.curve_combo.currentData()

    def generate_keys(self):
        try:
            pair = ecdh_generate_key_pair(self.selected_curve())
            self.private_key_edit.setPlainText(pair.private_key_pem)
            self.public_key_edit.setPlainText(pair.public_key_pem)
            QMessageBox.information(self, "Sukces", "Para kluczy została wygenerowana.")
            self.show_log_window()
        except Exception as exc:  # noqa: BLE001
            app_logger.error(f"ECDH generate error: {exc}")
            QMessageBox.critical(self, "Błąd", f"Nie udało się wygenerować kluczy:\n{exc}")

    def compute_secret(self):
        private_pem = self.private_key_edit.toPlainText().strip()
        peer_pem = self.peer_public_edit.toPlainText().strip()

        if not private_pem:
            QMessageBox.warning(self, "Brak klucza", "Najpierw wygeneruj lub wklej klucz prywatny.")
            return
        if not peer_pem:
            QMessageBox.warning(self, "Brak klucza partnera", "Wklej klucz publiczny partnera.")
            return

        try:
            result = ecdh_compute_shared_secret(
                private_key_pem=private_pem,
                peer_public_key_pem=peer_pem,
                curve_name=self.selected_curve(),
                hkdf_length=self.hkdf_length_spin.value(),
            )
            self.shared_secret_edit.setPlainText(result.shared_secret_hex)
            self.derived_key_edit.setPlainText(result.derived_key_hex)
            QMessageBox.information(
                self,
                "Sukces",
                "Wspólny sekret został obliczony. Możesz wykorzystać klucz HKDF np. do AES.",
            )
            self.show_log_window()
        except Exception as exc:  # noqa: BLE001
            app_logger.error(f"ECDH compute error: {exc}")
            QMessageBox.critical(self, "Błąd", f"Nie udało się uzgodnić sekretu:\n{exc}")

    def copy_text(self, text: str):
        if not text:
            QMessageBox.warning(self, "Brak danych", "Pole jest puste.")
            return
        clipboard = QApplication.clipboard()
        clipboard.setText(text)
        QMessageBox.information(self, "Skopiowano", "Tekst skopiowano do schowka.")

    def save_key_to_file(self, dialog_title: str, suggested_name: str, content: str):
        """Persist provided key material to PEM file."""
        content = content.strip()
        if not content:
            QMessageBox.warning(self, "Brak danych", "Najpierw wprowadź klucz do zapisu.")
            return
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            dialog_title,
            suggested_name,
            "Pliki PEM (*.pem);;Wszystkie pliki (*)",
        )
        if not file_path:
            return
        try:
            with open(file_path, "w", encoding="utf-8") as handle:
                handle.write(content)
            QMessageBox.information(self, "Zapisano", f"Klucz zapisano w {file_path}.")
        except OSError as exc:
            QMessageBox.critical(self, "Błąd zapisu", f"Nie udało się zapisać pliku:\n{exc}")

    def load_key_from_file(self, dialog_title: str, target_edit: QTextEdit):
        """Load PEM key from disk into the provided text field."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            dialog_title,
            "",
            "Pliki PEM (*.pem);;Wszystkie pliki (*)",
        )
        if not file_path:
            return
        try:
            with open(file_path, "r", encoding="utf-8") as handle:
                target_edit.setPlainText(handle.read())
            QMessageBox.information(self, "Wczytano", f"Załadowano klucz z {file_path}.")
        except OSError as exc:
            QMessageBox.critical(self, "Błąd odczytu", f"Nie udało się wczytać pliku:\n{exc}")

    def show_log_window(self):
        try:
            from views.log_viewer_window import LogViewerWindow

            self.log_window = LogViewerWindow(self)
            self.log_window.show()
        except Exception as exc:  # noqa: BLE001
            app_logger.error(f"ECDH log viewer error: {exc}")

    def go_back(self):
        if self.parent:
            self.parent.show()
        self.close()


