"""
Pomocnicza funkcja do wyświetlania okna logów
"""

from utils.logger import app_logger


def show_log_window(parent=None):
    """
    Wyświetla okno logów operacji
    
    Args:
        parent: Okno nadrzędne (opcjonalne)
    """
    try:
        from views.log_viewer_window import LogViewerWindow
        log_window = LogViewerWindow(parent)
        log_window.show()
        log_window.raise_()  # Przenieś okno na wierzch
        log_window.activateWindow()  # Aktywuj okno
        return log_window
    except Exception as e:
        app_logger.error(f"Error showing log window: {str(e)}")
        import traceback
        app_logger.error(f"Traceback: {traceback.format_exc()}")
        return None

