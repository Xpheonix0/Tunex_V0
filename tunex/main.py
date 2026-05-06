"""Entry point for the TuneX application."""

import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor
from tunex.ui.main_window import MainWindow


def _apply_dark_theme(app: QApplication) -> None:
    """Apply a dark, engineering-style palette and global stylesheet."""
    app.setStyle("Fusion")
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.ColorRole.Window, QColor(30, 30, 30))
    dark_palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
    dark_palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(40, 40, 40))
    dark_palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(45, 45, 45))
    dark_palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
    dark_palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
    dark_palette.setColor(QPalette.ColorRole.Button, QColor(45, 45, 45))
    dark_palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
    dark_palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
    dark_palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)
    app.setPalette(dark_palette)

    app.setStyleSheet("""
        QMainWindow { background-color: #1e1e1e; }
        QGroupBox { 
            color: #b0b0b0; 
            border: 1px solid #3c3c3c; 
            border-radius: 4px; 
            margin-top: 12px; 
            padding-top: 8px; 
        }
        QGroupBox::title { 
            subcontrol-origin: margin; 
            left: 10px; 
            padding: 0 5px; 
            color: #e0e0e0; 
        }
        QDoubleSpinBox, QSpinBox {
            background-color: #2b2b2b; 
            color: #ffffff; 
            border: 1px solid #555;
            padding: 2px;
        }
        QPushButton {
            background-color: #3a3a3a; 
            color: #ffffff; 
            border: 1px solid #555; 
            padding: 5px 14px; 
            border-radius: 3px;
        }
        QPushButton:hover { background-color: #4a4a4a; }
        QPushButton:pressed { background-color: #2a2a2a; }
        QCheckBox { color: #d0d0d0; }
        QLabel { color: #d0d0d0; }
        QStatusBar { color: #b0b0b0; background-color: #2a2a2a; }
    """)


def main() -> None:
    app = QApplication(sys.argv)
    _apply_dark_theme(app)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
