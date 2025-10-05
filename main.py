"""
Main application entry point for Matrix Determinant Calculator.
Uses Clean Architecture principles with separated layers and PyQt5.
"""
import logging
import sys
import os
from PyQt5.QtWidgets import QApplication

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from interfaces.gui import main as gui_main


def setup_logging():
    """Setup application-wide logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('determinant_calculator.log', encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Set specific log levels for different modules
    logging.getLogger('entities').setLevel(logging.DEBUG)
    logging.getLogger('use_cases').setLevel(logging.INFO)
    logging.getLogger('interfaces').setLevel(logging.INFO)


def main():
    """Main function to run the Matrix Determinant Calculator application."""
    try:
        # Setup logging
        setup_logging()
        logger = logging.getLogger(__name__)
        logger.info("Starting Matrix Determinant Calculator Application with PyQt5")
        
        # Run GUI application
        gui_main()
        
        logger.info("Application closed successfully")
        
    except Exception as e:
        logging.error(f"Fatal error in main: {str(e)}")
        print(f"Erro fatal: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
