"""
Main Window for PC Application
"""

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QTabWidget, QPushButton, QLabel, QFileDialog,
                             QTextEdit, QGroupBox, QProgressBar, QMessageBox)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QPixmap, QImage
import cv2
from utils.camera import CameraThread
from utils.api_client import APIClient

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.api_client = APIClient()
        self.camera_thread = None
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Cotton Leaf Disease Detection")
        self.setGeometry(100, 100, 1200, 800)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Title
        title = QLabel("Cotton Leaf Disease Detection System")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; padding: 20px;")
        layout.addWidget(title)
        
        # Tab widget
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)
        
        # Create tabs
        self.create_upload_tab()
        self.create_camera_tab()
        self.create_results_tab()
        
        # Status bar
        self.statusBar().showMessage("Ready")
        
    def create_upload_tab(self):
        """Create image upload tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)
        
        # Upload button
        upload_btn = QPushButton("Select Image")
        upload_btn.clicked.connect(self.select_image)
        upload_btn.setStyleSheet("padding: 10px; font-size: 14px;")
        layout.addWidget(upload_btn)
        
        # Image display
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumSize(640, 480)
        self.image_label.setStyleSheet("border: 2px solid #ccc; background: #f0f0f0;")
        layout.addWidget(self.image_label)
        
        # Analyze button
        self.analyze_btn = QPushButton("Analyze Image")
        self.analyze_btn.clicked.connect(self.analyze_image)
        self.analyze_btn.setEnabled(False)
        self.analyze_btn.setStyleSheet("padding: 10px; font-size: 14px;")
        layout.addWidget(self.analyze_btn)
        
        self.tabs.addTab(tab, "Upload Image")
        
    def create_camera_tab(self):
        """Create live camera tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)
        
        # Camera controls
        controls = QHBoxLayout()
        self.start_camera_btn = QPushButton("Start Camera")
        self.start_camera_btn.clicked.connect(self.toggle_camera)
        controls.addWidget(self.start_camera_btn)
        layout.addLayout(controls)
        
        # Camera feed
        self.camera_label = QLabel()
        self.camera_label.setAlignment(Qt.AlignCenter)
        self.camera_label.setMinimumSize(640, 480)
        self.camera_label.setStyleSheet("border: 2px solid #ccc; background: #000;")
        layout.addWidget(self.camera_label)
        
        self.tabs.addTab(tab, "Live Camera")
        
    def create_results_tab(self):
        """Create results display tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)
        
        # Results text area
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        layout.addWidget(self.results_text)
        
        self.tabs.addTab(tab, "Results")
        
    def select_image(self):
        """Open file dialog to select image"""
        filename, _ = QFileDialog.getOpenFileName(
            self, "Select Image", "", "Images (*.png *.jpg *.jpeg *.bmp)"
        )
        if filename:
            self.current_image_path = filename
            pixmap = QPixmap(filename)
            self.image_label.setPixmap(pixmap.scaled(
                self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
            ))
            self.analyze_btn.setEnabled(True)
            self.statusBar().showMessage(f"Loaded: {filename}")
            
    def analyze_image(self):
        """Send image to API for analysis"""
        if not hasattr(self, 'current_image_path'):
            return
            
        self.statusBar().showMessage("Analyzing...")
        self.analyze_btn.setEnabled(False)
        
        try:
            result = self.api_client.predict_image(self.current_image_path)
            self.display_results(result)
            self.statusBar().showMessage("Analysis complete")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Analysis failed: {str(e)}")
            self.statusBar().showMessage("Analysis failed")
        finally:
            self.analyze_btn.setEnabled(True)
            
    def toggle_camera(self):
        """Start/stop camera"""
        if self.camera_thread is None or not self.camera_thread.isRunning():
            self.camera_thread = CameraThread()
            self.camera_thread.frame_ready.connect(self.update_camera_frame)
            self.camera_thread.start()
            self.start_camera_btn.setText("Stop Camera")
        else:
            self.camera_thread.stop()
            self.camera_thread = None
            self.start_camera_btn.setText("Start Camera")
            
    def update_camera_frame(self, frame):
        """Update camera display with new frame"""
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_image)
        self.camera_label.setPixmap(pixmap.scaled(
            self.camera_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
        ))
        
    def display_results(self, results):
        """Display analysis results"""
        self.tabs.setCurrentIndex(2)  # Switch to results tab
        
        text = "=== Analysis Results ===\n\n"
        text += f"Detections: {results['num_detections']}\n"
        text += f"Inference Time: {results['inference_time_ms']:.1f}ms\n\n"
        
        text += "=== Severity ===\n"
        severity = results['severity']
        text += f"Category: {severity['category']}\n"
        text += f"Percentage: {severity['percentage']:.1f}%\n"
        text += f"Description: {severity['description']}\n\n"
        
        text += "=== Detected Diseases ===\n"
        for det in results['detections']:
            text += f"- {det['class_name']}: {det['confidence']*100:.1f}%\n"
        
        text += "\n=== Recommendations ===\n"
        for rec in results['recommendations']:
            text += f"\n[{rec['priority'].upper()}] {rec['title']}\n"
            text += f"{rec['description']}\n"
        
        self.results_text.setText(text)
