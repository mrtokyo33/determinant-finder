"""
GUI interface using PyQt5 for matrix determinant calculator with modern dark theme.
"""
import sys
import logging
from typing import List, Optional
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QGridLayout, QLabel, QLineEdit, 
                            QComboBox, QPushButton, QMessageBox, QFrame,
                            QSizePolicy, QSpacerItem, QScrollArea, QSpinBox)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QFont, QPalette, QColor, QLinearGradient, QBrush, QWheelEvent, QTransform
from use_cases.calculate_determinant_use_case import CalculateDeterminantUseCase

logger = logging.getLogger(__name__)


class MatrixDeterminantGUI(QMainWindow):
    """GUI for matrix determinant calculator with modern dark theme using PyQt5."""
    
    def __init__(self):
        """Initialize the GUI application."""
        super().__init__()
        
        # Dark theme colors
        self.colors = {
            'bg_primary': '#1a1a1a',      # Very dark background
            'bg_secondary': '#2d2d2d',     # Slightly lighter gray
            'accent_blue': '#0078d4',      # Electric blue
            'accent_blue_light': '#106ebe', # Lighter blue
            'text_primary': '#ffffff',     # White text
            'text_secondary': '#cccccc',   # Light gray text
            'entry_bg': '#3c3c3c',        # Dark entry background
            'border': '#404040',           # Gray border
            'success_green': '#00ff41'     # Success green
        }
        
        # Use case
        self.calculate_use_case = CalculateDeterminantUseCase()
        
        # GUI components
        self.matrix_entries: List[List[QLineEdit]] = []
        self.matrix_size_spinbox: Optional[QSpinBox] = None
        self.calculate_button: Optional[QPushButton] = None
        self.result_label: Optional[QLabel] = None
        self.matrix_widget: Optional[QWidget] = None
        self.matrix_scroll: Optional[QScrollArea] = None
        
        # Zoom variables
        self.zoom_factor = 1.0
        self.min_zoom = 0.3
        self.max_zoom = 3.0
        self.zoom_step = 0.1
        
        self._setup_logging()
        self._setup_ui()
        
        logger.info("Matrix Determinant GUI initialized with PyQt5 dark theme")
    
    def _setup_logging(self):
        """Setup logging configuration."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('determinant_calculator.log'),
                logging.StreamHandler()
            ]
        )
    
    def _setup_ui(self):
        """Setup the user interface."""
        self.setWindowTitle("Calculadora de Determinante - Escalonamento")
        self.setGeometry(100, 100, 1000, 700)
        
        # Set dark theme
        self._apply_dark_theme()
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # Title
        title_label = QLabel("Calculadora de Determinante")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(f"""
            QLabel {{
                color: {self.colors['text_primary']};
                font-size: 28px;
                font-weight: bold;
                margin-bottom: 10px;
            }}
        """)
        main_layout.addWidget(title_label)
        
        # Instructions
        instructions_label = QLabel("💡 Dica: Use Ctrl + Scroll para fazer zoom na matriz")
        instructions_label.setAlignment(Qt.AlignCenter)
        instructions_label.setStyleSheet(f"""
            QLabel {{
                color: {self.colors['text_secondary']};
                font-size: 12px;
                font-style: italic;
                margin-bottom: 10px;
            }}
        """)
        main_layout.addWidget(instructions_label)
        
        
        # Top control area
        top_layout = QHBoxLayout()
        top_layout.addStretch()
        
        # Matrix size selection
        size_label = QLabel("Ordem da Matriz:")
        size_label.setStyleSheet(f"""
            QLabel {{
                color: {self.colors['text_primary']};
                font-size: 16px;
                font-weight: bold;
            }}
        """)
        top_layout.addWidget(size_label)
        
        self.matrix_size_spinbox = QSpinBox()
        self.matrix_size_spinbox.setMinimum(2)
        self.matrix_size_spinbox.setMaximum(50)  # Allow up to 50x50 matrix
        self.matrix_size_spinbox.setValue(3)
        self.matrix_size_spinbox.setStyleSheet(f"""
            QSpinBox {{
                background-color: {self.colors['entry_bg']};
                color: {self.colors['text_primary']};
                border: 2px solid {self.colors['accent_blue']};
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 14px;
                min-width: 80px;
            }}
            QSpinBox::up-button {{
                background-color: {self.colors['accent_blue']};
                border: none;
                border-radius: 3px;
                width: 20px;
            }}
            QSpinBox::up-button:hover {{
                background-color: {self.colors['accent_blue_light']};
            }}
            QSpinBox::down-button {{
                background-color: {self.colors['accent_blue']};
                border: none;
                border-radius: 3px;
                width: 20px;
            }}
            QSpinBox::down-button:hover {{
                background-color: {self.colors['accent_blue_light']};
            }}
        """)
        self.matrix_size_spinbox.valueChanged.connect(self._on_size_changed)
        top_layout.addWidget(self.matrix_size_spinbox)
        
        # Zoom indicator
        self.zoom_label = QLabel("Zoom: 100%")
        self.zoom_label.setStyleSheet(f"""
            QLabel {{
                color: {self.colors['text_secondary']};
                font-size: 12px;
                font-weight: bold;
            }}
        """)
        top_layout.addWidget(self.zoom_label)
        
        top_layout.addStretch()
        main_layout.addLayout(top_layout)
        
        # Matrix area with scroll and zoom
        self.matrix_scroll = QScrollArea()
        self.matrix_scroll.setWidgetResizable(True)
        self.matrix_scroll.setStyleSheet(f"""
            QScrollArea {{
                background-color: {self.colors['bg_primary']};
                border: none;
            }}
        """)
        # Enable wheel events for zoom
        self.matrix_scroll.wheelEvent = self._on_wheel_event
        
        # Create matrix container widget
        self.matrix_container = QWidget()
        self.matrix_container.setStyleSheet(f"""
            QWidget {{
                background-color: {self.colors['bg_primary']};
            }}
        """)
        self.matrix_scroll.setWidget(self.matrix_container)
        
        # Create matrix layout
        self.matrix_layout = QVBoxLayout(self.matrix_container)
        self.matrix_layout.setAlignment(Qt.AlignCenter)
        
        # Create matrix grid widget
        self.matrix_widget = QWidget()
        self.matrix_widget.setStyleSheet(f"""
            QWidget {{
                background-color: {self.colors['bg_primary']};
            }}
        """)
        self.matrix_layout.addWidget(self.matrix_widget)
        
        main_layout.addWidget(self.matrix_scroll, 1)
        
        # Bottom area with button
        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()
        
        self.calculate_button = QPushButton("Achar Determinante")
        self.calculate_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.colors['accent_blue']};
                color: {self.colors['text_primary']};
                border: none;
                border-radius: 12px;
                padding: 15px 30px;
                font-size: 16px;
                font-weight: bold;
                min-width: 200px;
            }}
            QPushButton:hover {{
                background-color: {self.colors['accent_blue_light']};
            }}
            QPushButton:pressed {{
                background-color: {self.colors['accent_blue_light']};
            }}
        """)
        self.calculate_button.clicked.connect(self._calculate_determinant)
        bottom_layout.addWidget(self.calculate_button)
        
        bottom_layout.addStretch()
        main_layout.addLayout(bottom_layout)
        
        # Result label (initially hidden)
        self.result_label = QLabel("")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet(f"""
            QLabel {{
                color: {self.colors['success_green']};
                font-size: 24px;
                font-weight: bold;
                background-color: {self.colors['bg_secondary']};
                border: 2px solid {self.colors['accent_blue']};
                border-radius: 12px;
                padding: 20px;
                margin: 20px;
            }}
        """)
        self.result_label.hide()
        main_layout.addWidget(self.result_label)
        
        # Create initial matrix
        self._create_matrix_entries()
    
    def _apply_dark_theme(self):
        """Apply dark theme to the application."""
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(self.colors['bg_primary']))
        palette.setColor(QPalette.WindowText, QColor(self.colors['text_primary']))
        palette.setColor(QPalette.Base, QColor(self.colors['entry_bg']))
        palette.setColor(QPalette.AlternateBase, QColor(self.colors['bg_secondary']))
        palette.setColor(QPalette.ToolTipBase, QColor(self.colors['text_primary']))
        palette.setColor(QPalette.ToolTipText, QColor(self.colors['text_primary']))
        palette.setColor(QPalette.Text, QColor(self.colors['text_primary']))
        palette.setColor(QPalette.Button, QColor(self.colors['accent_blue']))
        palette.setColor(QPalette.ButtonText, QColor(self.colors['text_primary']))
        palette.setColor(QPalette.BrightText, QColor(self.colors['success_green']))
        palette.setColor(QPalette.Link, QColor(self.colors['accent_blue']))
        palette.setColor(QPalette.Highlight, QColor(self.colors['accent_blue']))
        palette.setColor(QPalette.HighlightedText, QColor(self.colors['text_primary']))
        
        self.setPalette(palette)
    
    def _on_size_changed(self):
        """Handle matrix size change."""
        size = self.matrix_size_spinbox.value()
        logger.info(f"Matrix size changed to: {size}")
        self._create_matrix_entries()
    
    def _create_matrix_entries(self):
        """Create matrix input entries based on selected size with dark theme."""
        # Clear existing entries
        for widget in self.matrix_widget.findChildren(QLineEdit):
            widget.deleteLater()
        self.matrix_entries.clear()
        
        # Remove matrix widget from layout
        self.matrix_layout.removeWidget(self.matrix_widget)
        self.matrix_widget.deleteLater()
        
        # Create new matrix widget
        self.matrix_widget = QWidget()
        self.matrix_widget.setStyleSheet(f"""
            QWidget {{
                background-color: {self.colors['bg_primary']};
            }}
        """)
        
        try:
            size = self.matrix_size_spinbox.value()
            if size < 2 or size > 50:
                QMessageBox.warning(self, "Erro", "Tamanho da matriz deve estar entre 2 e 50")
                return
            
            logger.info(f"Creating matrix entries for {size}x{size} matrix")
            
            # Create grid layout for matrix
            matrix_grid = QGridLayout()
            matrix_grid.setSpacing(10)
            matrix_grid.setContentsMargins(20, 20, 20, 20)
            
            # Create entries with dark theme
            for i in range(size):
                row_entries = []
                for j in range(size):
                    entry = QLineEdit()
                    entry.setAlignment(Qt.AlignCenter)
                    entry.setText("0")
                    entry.setMaxLength(10)
                    entry.setStyleSheet(f"""
                        QLineEdit {{
                            background-color: {self.colors['entry_bg']};
                            color: {self.colors['text_primary']};
                            border: 2px solid {self.colors['border']};
                            border-radius: 8px;
                            padding: 8px;
                            font-size: 14px;
                            font-weight: bold;
                            min-width: 60px;
                            max-width: 80px;
                        }}
                        QLineEdit:focus {{
                            border-color: {self.colors['accent_blue']};
                        }}
                    """)
                    
                    # Connect signals for better UX
                    entry.returnPressed.connect(self._focus_next_entry)
                    entry.textChanged.connect(lambda: self._on_entry_changed())
                    
                    matrix_grid.addWidget(entry, i, j)
                    row_entries.append(entry)
                self.matrix_entries.append(row_entries)
            
            # Center the matrix
            matrix_grid.setAlignment(Qt.AlignCenter)
            
            # Set the layout to the widget
            self.matrix_widget.setLayout(matrix_grid)
            
            # Add matrix widget back to layout
            self.matrix_layout.addWidget(self.matrix_widget)
            
            # Force update
            self.matrix_widget.update()
            self.update()
            
        except ValueError:
            QMessageBox.warning(self, "Erro", "Tamanho da matriz deve ser um número válido")
    
    def _on_entry_changed(self):
        """Handle entry text change."""
        pass
    
    def _on_wheel_event(self, event: QWheelEvent):
        """Handle wheel event for zooming."""
        # Check if Ctrl key is pressed for zoom
        if event.modifiers() & Qt.ControlModifier:
            # Get wheel delta
            delta = event.angleDelta().y()
            
            if delta > 0:  # Zoom in
                self.zoom_factor = min(self.zoom_factor + self.zoom_step, self.max_zoom)
            else:  # Zoom out
                self.zoom_factor = max(self.zoom_factor - self.zoom_step, self.min_zoom)
            
            # Apply zoom
            self._apply_zoom()
            event.accept()
        else:
            # Normal scroll behavior
            QScrollArea.wheelEvent(self.matrix_scroll, event)
    
    def _apply_zoom(self):
        """Apply zoom to the matrix widget."""
        if self.matrix_widget:
            # Update zoom indicator
            zoom_percentage = int(self.zoom_factor * 100)
            self.zoom_label.setText(f"Zoom: {zoom_percentage}%")
            
            # Apply zoom by scaling font sizes and spacing
            font_size = int(14 * self.zoom_factor)
            padding = int(8 * self.zoom_factor)
            min_width = int(60 * self.zoom_factor)
            max_width = int(80 * self.zoom_factor)
            
            # Update matrix widget style
            self.matrix_widget.setStyleSheet(f"""
                QWidget {{
                    background-color: {self.colors['bg_primary']};
                    transform: scale({self.zoom_factor});
                }}
            """)
            
            # Update entry styles
            for row_entries in self.matrix_entries:
                for entry in row_entries:
                    entry.setStyleSheet(f"""
                        QLineEdit {{
                            background-color: {self.colors['entry_bg']};
                            color: {self.colors['text_primary']};
                            border: 2px solid {self.colors['border']};
                            border-radius: 8px;
                            padding: {padding}px;
                            font-size: {font_size}px;
                            font-weight: bold;
                            min-width: {min_width}px;
                            max-width: {max_width}px;
                        }}
                        QLineEdit:focus {{
                            border-color: {self.colors['accent_blue']};
                        }}
                    """)
            
            # Update scroll area
            self.matrix_scroll.update()
            
            logger.debug(f"Zoom applied: {self.zoom_factor:.2f}x")
    
    def wheelEvent(self, event: QWheelEvent):
        """Override wheel event for the main window."""
        # Check if mouse is over matrix area
        if self.matrix_scroll.underMouse():
            self._on_wheel_event(event)
        else:
            super().wheelEvent(event)
    
    def _focus_next_entry(self):
        """Focus next entry in tab order."""
        # Simple tab order: left to right, top to bottom
        current_widget = self.focusWidget()
        
        for i, row_entries in enumerate(self.matrix_entries):
            for j, entry in enumerate(row_entries):
                if entry == current_widget:
                    # Find next entry
                    if j < len(row_entries) - 1:
                        row_entries[j + 1].setFocus()
                    elif i < len(self.matrix_entries) - 1:
                        self.matrix_entries[i + 1][0].setFocus()
                    else:
                        # Last entry, focus calculate button
                        self.calculate_button.setFocus()
                    return
    
    def _get_matrix_data(self) -> List[List[float]]:
        """Extract matrix data from input entries."""
        matrix_data = []
        
        for row_entries in self.matrix_entries:
            row_data = []
            for entry in row_entries:
                try:
                    value = float(entry.text())
                    row_data.append(value)
                except ValueError:
                    raise ValueError("Todos os elementos devem ser números válidos")
            matrix_data.append(row_data)
        
        return matrix_data
    
    def _calculate_determinant(self):
        """Calculate matrix determinant and display result."""
        try:
            logger.info("Starting determinant calculation")
            
            # Hide previous result
            self.result_label.hide()
            
            # Get matrix data
            matrix_data = self._get_matrix_data()
            
            # Validate matrix
            is_valid, error_msg = self.calculate_use_case.validate_matrix_data(matrix_data)
            if not is_valid:
                QMessageBox.warning(self, "Erro de Validação", error_msg)
                return
            
            # Calculate determinant
            determinant, steps = self.calculate_use_case.execute(matrix_data)
            
            # Show result
            self._show_result(determinant)
            
            logger.info(f"Determinant calculation completed: {determinant}")
            
        except ValueError as e:
            error_msg = str(e)
            QMessageBox.warning(self, "Erro", error_msg)
            logger.error(f"Value error in calculation: {error_msg}")
            
        except Exception as e:
            error_msg = f"Erro inesperado: {str(e)}"
            QMessageBox.warning(self, "Erro", error_msg)
            logger.error(f"Unexpected error in calculation: {str(e)}")
    
    def _show_result(self, determinant: float):
        """Show result with animation."""
        result_text = f"Determinante = {determinant:.6f}"
        self.result_label.setText(result_text)
        self.result_label.show()
        
        # Auto-hide after 5 seconds
        QTimer.singleShot(5000, self._hide_result)
    
    def _hide_result(self):
        """Hide the result."""
        self.result_label.hide()


def main():
    """Main function to run the application."""
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Calculadora de Determinante")
    app.setApplicationVersion("1.0")
    
    # Create and show main window
    window = MatrixDeterminantGUI()
    window.show()
    
    # Start event loop
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
