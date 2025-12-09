"""
Okno hashowania i weryfikacji plików algorytmem SHA-256.
"""

import binascii
from PyQt5.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QFileDialog,
    QTextEdit,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from utils.sha256_utils import hash_file, verify_file


def _salt_from_hex(text: str):
    if not text:
        return None
    try:
        return bytes.fromhex(text.strip())
    except (ValueError, binascii.Error):
        raise ValueError("Sól musi być podana w formacie hex.")


class Sha256FileWindow(QMainWindow):
    """Okno hashowania/weryfikacji plików SHA-256."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()
        self.setup_styles()

    def init_ui(self):
        self.setWindowTitle("SHA-256 - Pliki")
        self.setGeometry(200, 200, 800, 750)
        self.setMinimumSize(700, 600)
        self.showMaximized()

        central_widget = QFrame()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(25, 25, 25, 25)

        title = QLabel("🔒 SHA-256 - Pliki")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                padding: 14px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #16a085, stop:1 #149174);
                border-radius: 12px;
                color: white;
            }
        """)
        main_layout.addWidget(title)

        # Hash
        hash_frame = QFrame()
        hash_frame.setFrameStyle(QFrame.StyledPanel)
        hash_frame.setStyleSheet("""
            QFrame {
                background: #f8f9fa;
                border: 2px solid #e9ecef;
                border-radius: 12px;
                padding: 12px;
            }
        """)
        hash_layout = QVBoxLayout(hash_frame)

        hash_label = QLabel("Hashuj plik (SHA-256)")
        hash_label.setFont(QFont("Arial", 14, QFont.Bold))
        hash_layout.addWidget(hash_label)

        file_select_layout = QHBoxLayout()
        self.hash_file_path = QLineEdit()
        self.hash_file_path.setPlaceholderText("Ścieżka do pliku...")
        self.hash_file_path.setReadOnly(True)
        file_select_layout.addWidget(self.hash_file_path)
        browse_hash_btn = QPushButton("📂 Wybierz plik")
        browse_hash_btn.clicked.connect(self.browse_hash_file)
        file_select_layout.addWidget(browse_hash_btn)
        hash_layout.addLayout(file_select_layout)

        salt_label = QLabel("Sól (hex, opcjonalnie; jeśli puste wygenerujemy losową)")
        hash_layout.addWidget(salt_label)
        self.hash_salt_input = QLineEdit()
        self.hash_salt_input.setPlaceholderText("np. 1f2d3c4b...")
        hash_layout.addWidget(self.hash_salt_input)

        self.hash_button = QPushButton("🔒 Oblicz hash")
        self.hash_button.clicked.connect(self.on_hash_clicked)
        self.hash_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #16a085, stop:1 #13856f);
                color: white; border: none; border-radius: 8px; padding: 10px;
                font-size: 14px; font-weight: bold;
            }
            QPushButton:hover { background: #13856f; }
        """)
        hash_layout.addWidget(self.hash_button)

        self.hash_result = QTextEdit()
        self.hash_result.setReadOnly(True)
        self.hash_result.setMinimumHeight(90)
        hash_layout.addWidget(self.hash_result)

        main_layout.addWidget(hash_frame)

        # Verify
        verify_frame = QFrame()
        verify_frame.setFrameStyle(QFrame.StyledPanel)
        verify_frame.setStyleSheet("""
            QFrame {
                background: #f8f9fa;
                border: 2px solid #e9ecef;
                border-radius: 12px;
                padding: 12px;
            }
        """)
        verify_layout = QVBoxLayout(verify_frame)

        verify_label = QLabel("Weryfikuj hash pliku (SHA-256)")
        verify_label.setFont(QFont("Arial", 14, QFont.Bold))
        verify_layout.addWidget(verify_label)

        verify_select_layout = QHBoxLayout()
        self.verify_file_path = QLineEdit()
        self.verify_file_path.setPlaceholderText("Ścieżka do pliku...")
        self.verify_file_path.setReadOnly(True)
        verify_select_layout.addWidget(self.verify_file_path)
        browse_verify_btn = QPushButton("📂 Wybierz plik")
        browse_verify_btn.clicked.connect(self.browse_verify_file)
        verify_select_layout.addWidget(browse_verify_btn)
        verify_layout.addLayout(verify_select_layout)

        self.verify_hash_input = QLineEdit()
        self.verify_hash_input.setPlaceholderText("Oczekiwany hash (hex)")
        verify_layout.addWidget(self.verify_hash_input)

        self.verify_salt_input = QLineEdit()
        self.verify_salt_input.setPlaceholderText("Sól (hex) użyta przy hashowaniu")
        verify_layout.addWidget(self.verify_salt_input)

        self.verify_button = QPushButton("✅ Sprawdź")
        self.verify_button.clicked.connect(self.on_verify_clicked)
        self.verify_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2980b9, stop:1 #21618c);
                color: white; border: none; border-radius: 8px; padding: 10px;
                font-size: 14px; font-weight: bold;
            }
            QPushButton:hover { background: #21618c; }
        """)
        verify_layout.addWidget(self.verify_button)

        self.verify_result = QLabel("")
        self.verify_result.setAlignment(Qt.AlignLeft)
        self.verify_result.setStyleSheet("QLabel { color: #2c3e50; font-weight: bold; }")
        verify_layout.addWidget(self.verify_result)

        main_layout.addWidget(verify_frame)

        # Footer
        footer_layout = QHBoxLayout()
        self.clear_button = QPushButton("🗑️ Wyczyść")
        self.clear_button.clicked.connect(self.clear_all)
        footer_layout.addWidget(self.clear_button)

        self.back_button = QPushButton("⬅️ Powrót")
        self.back_button.clicked.connect(self.go_back)
        footer_layout.addWidget(self.back_button)

        footer_layout.addStretch()
        main_layout.addLayout(footer_layout)

    def setup_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #ecf0f1, stop:1 #bdc3c7);
            }
        """)

    def browse_hash_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Wybierz plik do hashowania", "", "Wszystkie pliki (*.*)")
        if path:
            self.hash_file_path.setText(path)

    def browse_verify_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Wybierz plik do weryfikacji", "", "Wszystkie pliki (*.*)")
        if path:
            self.verify_file_path.setText(path)

    def on_hash_clicked(self):
        path = self.hash_file_path.text().strip()
        if not path:
            QMessageBox.warning(self, "Błąd", "Wybierz plik do hashowania.")
            return
        try:
            salt = _salt_from_hex(self.hash_salt_input.text().strip())
            digest, salt_bytes = hash_file(path, salt)
            self.hash_result.setPlainText(f"hash: {digest}\nsalt: {salt_bytes.hex()}")
        except ValueError as exc:
            QMessageBox.warning(self, "Błąd", str(exc))
        except Exception as exc:
            QMessageBox.critical(self, "Błąd", f"Nie udało się obliczyć hash: {exc}")

    def on_verify_clicked(self):
        path = self.verify_file_path.text().strip()
        expected = self.verify_hash_input.text().strip()
        salt_hex = self.verify_salt_input.text().strip()
        if not (path and expected and salt_hex):
            QMessageBox.warning(self, "Błąd", "Podaj plik, hash oraz sól (hex).")
            return
        try:
            salt = _salt_from_hex(salt_hex)
            ok = verify_file(path, expected, salt)
            if ok:
                self.verify_result.setText("✅ Hash pliku pasuje.")
                self.verify_result.setStyleSheet("QLabel { color: #27ae60; font-weight: bold; }")
            else:
                self.verify_result.setText("❌ Hash pliku nie pasuje.")
                self.verify_result.setStyleSheet("QLabel { color: #e74c3c; font-weight: bold; }")
        except ValueError as exc:
            QMessageBox.warning(self, "Błąd", str(exc))
        except Exception as exc:
            QMessageBox.critical(self, "Błąd", f"Nie udało się zweryfikować hash: {exc}")

    def clear_all(self):
        self.hash_file_path.clear()
        self.hash_salt_input.clear()
        self.hash_result.clear()
        self.verify_file_path.clear()
        self.verify_hash_input.clear()
        self.verify_salt_input.clear()
        self.verify_result.setText("")

    def go_back(self):
        if self.parent:
            self.parent.show()
        self.close()


def main():
    app = QApplication([])
    w = Sha256FileWindow()
    w.show()
    app.exec_()


if __name__ == "__main__":
    main()

