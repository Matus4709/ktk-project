"""
Okno przeglądarki logów operacji szyfrowania/deszyfrowania
"""

import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                             QWidget, QLabel, QTextEdit, QPushButton, QFrame,
                             QMessageBox, QScrollArea)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont, QTextCharFormat, QTextCursor, QColor
from utils.logger import app_logger


class LogViewerWindow(QMainWindow):
    """Okno do wyświetlania szczegółowych logów operacji"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.init_ui()
        self.load_last_log()
        
    def init_ui(self):
        """Inicjalizacja interfejsu użytkownika"""
        self.setWindowTitle("📋 Logi Operacji - Analiza Krok po Kroku")
        self.setGeometry(100, 100, 1000, 700)
        self.setMinimumSize(800, 600)
        
        # Główny widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Główny layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Tytuł
        title_frame = QFrame()
        title_frame.setFrameStyle(QFrame.StyledPanel)
        title_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #3498db, stop:1 #2980b9);
                border-radius: 10px;
                padding: 15px;
            }
        """)
        title_layout = QVBoxLayout(title_frame)
        
        title_label = QLabel("📋 Analiza Logów Operacji")
        title_label.setAlignment(Qt.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: white;")
        title_layout.addWidget(title_label)
        
        subtitle_label = QLabel("Szczegółowe wyjaśnienie działania algorytmu krok po kroku z przykładami danych")
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("color: white; font-size: 12px;")
        title_layout.addWidget(subtitle_label)
        
        main_layout.addWidget(title_frame)
        
        # Przyciski kontrolne
        control_frame = QFrame()
        control_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        control_layout = QHBoxLayout(control_frame)
        
        self.refresh_button = QPushButton("🔄 Odśwież")
        self.refresh_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #17a2b8, stop:1 #138496);
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #138496, stop:1 #0f6674);
            }
        """)
        self.refresh_button.clicked.connect(self.load_last_log)
        control_layout.addWidget(self.refresh_button)
        
        self.all_logs_button = QPushButton("📚 Wszystkie logi")
        self.all_logs_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #6c757d, stop:1 #495057);
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #495057, stop:1 #343a40);
            }
        """)
        self.all_logs_button.clicked.connect(self.show_all_logs)
        control_layout.addWidget(self.all_logs_button)
        
        self.clear_button = QPushButton("🗑️ Wyczyść logi")
        self.clear_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #dc3545, stop:1 #c82333);
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #c82333, stop:1 #bd2130);
            }
        """)
        self.clear_button.clicked.connect(self.clear_logs)
        control_layout.addWidget(self.clear_button)
        
        self.copy_button = QPushButton("📋 Kopiuj")
        self.copy_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #28a745, stop:1 #1e7e34);
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1e7e34, stop:1 #155724);
            }
        """)
        self.copy_button.clicked.connect(self.copy_to_clipboard)
        control_layout.addWidget(self.copy_button)
        
        control_layout.addStretch()
        
        self.close_button = QPushButton("✕ Zamknij")
        self.close_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #6c757d, stop:1 #495057);
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #495057, stop:1 #343a40);
            }
        """)
        self.close_button.clicked.connect(self.close)
        control_layout.addWidget(self.close_button)
        
        main_layout.addWidget(control_frame)
        
        # Obszar logów
        log_frame = QFrame()
        log_frame.setFrameStyle(QFrame.StyledPanel)
        log_frame.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border: 2px solid #dee2e6;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        log_layout = QVBoxLayout(log_frame)
        
        log_label = QLabel("📝 Szczegółowy log operacji:")
        log_label.setStyleSheet("font-weight: bold; color: #2c3e50; font-size: 14px; margin-bottom: 10px;")
        log_layout.addWidget(log_label)
        
        # Tekst z logami
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet("""
            QTextEdit {
                border: 1px solid #ced4da;
                border-radius: 8px;
                padding: 15px;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 11px;
                background-color: #ffffff;
                color: #212529;
                line-height: 1.4;
            }
        """)
        self.log_text.setMinimumHeight(500)
        log_layout.addWidget(self.log_text)
        
        main_layout.addWidget(log_frame)
        
        # Ustawienie stylu głównego okna
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f8f9fa, stop:1 #e9ecef);
            }
        """)
    
    def load_last_log(self):
        """Ładuje ostatni log operacji"""
        try:
            log = app_logger.get_last_operation_log()
            if log:
                formatted_log = app_logger.format_log_for_display(log)
                self.log_text.setPlainText(formatted_log)
                self.highlight_log_text()
            else:
                # Sprawdź wszystkie logi dla debugowania
                all_logs = app_logger.get_all_logs()
                if all_logs:
                    # Jeśli są logi, ale get_last_operation_log zwraca None, użyj ostatniego
                    log = all_logs[-1]
                    formatted_log = app_logger.format_log_for_display(log)
                    self.log_text.setPlainText(formatted_log)
                    self.highlight_log_text()
                else:
                    self.log_text.setPlainText(
                        "Brak dostępnych logów operacji.\n\n"
                        "Logi pojawią się tutaj po wykonaniu operacji szyfrowania lub deszyfrowania."
                    )
        except Exception as e:
            import traceback
            error_msg = f"Błąd podczas ładowania logów: {str(e)}\n\n{traceback.format_exc()}"
            self.log_text.setPlainText(error_msg)
            app_logger.error(f"Error loading log: {str(e)}")
            app_logger.error(f"Traceback: {traceback.format_exc()}")
    
    def show_all_logs(self):
        """Wyświetla wszystkie zapisane logi"""
        all_logs = app_logger.get_all_logs()
        if not all_logs:
            QMessageBox.information(self, "Informacja", "Brak zapisanych logów.")
            return
        
        # Formatuj wszystkie logi
        formatted_logs = []
        for i, log in enumerate(reversed(all_logs), 1):  # Od najnowszych
            formatted_logs.append(f"\n{'='*80}\n")
            formatted_logs.append(f"LOG #{i}\n")
            formatted_logs.append(app_logger.format_log_for_display(log))
        
        self.log_text.setPlainText("\n".join(formatted_logs))
        self.highlight_log_text()
    
    def highlight_log_text(self):
        """Podświetla różne typy logów różnymi kolorami"""
        # Pobierz tekst
        text = self.log_text.toPlainText()
        
        # Ustaw formatowanie
        cursor = self.log_text.textCursor()
        cursor.movePosition(QTextCursor.Start)
        
        # Kolorowanie różnych typów linii
        lines = text.split('\n')
        for i, line in enumerate(lines):
            if '▶' in line or 'START' in line:
                # Start - niebieski
                self.set_line_color(i, QColor(0, 102, 204))
            elif '✓' in line or 'SUCCESS' in line:
                # Sukces - zielony
                self.set_line_color(i, QColor(0, 153, 0))
            elif '✗' in line or 'ERROR' in line:
                # Błąd - czerwony
                self.set_line_color(i, QColor(204, 0, 0))
            elif '⚠' in line or 'WARNING' in line:
                # Ostrzeżenie - pomarańczowy
                self.set_line_color(i, QColor(255, 153, 0))
            elif '→' in line or 'STEP' in line:
                # Krok - czarny
                self.set_line_color(i, QColor(0, 0, 0))
            elif 'ℹ' in line or 'INFO' in line:
                # Info - szary
                self.set_line_color(i, QColor(102, 102, 102))
            elif '📝' in line or 'EXPLANATION' in line or 'Opis algorytmu' in line:
                # Wyjaśnienie - niebieski
                self.set_line_color(i, QColor(0, 102, 204))
    
    def set_line_color(self, line_number: int, color: QColor):
        """Ustawia kolor dla określonej linii"""
        cursor = self.log_text.textCursor()
        cursor.movePosition(QTextCursor.Start)
        
        # Przejdź do linii
        for _ in range(line_number):
            cursor.movePosition(QTextCursor.Down)
        
        # Wybierz całą linię
        cursor.movePosition(QTextCursor.StartOfLine)
        cursor.movePosition(QTextCursor.EndOfLine, QTextCursor.KeepAnchor)
        
        # Ustaw format
        format = QTextCharFormat()
        format.setForeground(color)
        cursor.setCharFormat(format)
    
    def clear_logs(self):
        """Czyści wszystkie logi"""
        reply = QMessageBox.question(
            self, 
            "Potwierdzenie", 
            "Czy na pewno chcesz wyczyścić wszystkie logi?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            app_logger.clear_logs()
            self.log_text.setPlainText("Logi zostały wyczyszczone.")
            QMessageBox.information(self, "Sukces", "Wszystkie logi zostały wyczyszczone.")
    
    def copy_to_clipboard(self):
        """Kopiuje zawartość logów do schowka"""
        text = self.log_text.toPlainText()
        if text:
            clipboard = QApplication.clipboard()
            clipboard.setText(text)
            QMessageBox.information(self, "Sukces", "Logi zostały skopiowane do schowka!")
        else:
            QMessageBox.warning(self, "Uwaga", "Brak logów do skopiowania.")
    
    def closeEvent(self, event):
        """Obsługa zamknięcia okna - czyści zawartość okna"""
        # Czyść zawartość okna po zamknięciu
        self.log_text.clear()
        event.accept()


def main():
    """Funkcja główna dla testowania"""
    app = QApplication(sys.argv)
    window = LogViewerWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

