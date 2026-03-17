"""
Cotton Leaf Disease Detection - PC Application
PyQt5 Desktop Application for real-time disease detection
"""

import sys
from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow

def main():
    """Main entry point for the application"""
    app = QApplication(sys.argv)
    app.setApplicationName("Cotton Disease Detection")
    app.setOrganizationName("AgriTech")
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
