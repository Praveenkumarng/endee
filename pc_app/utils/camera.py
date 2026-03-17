"""
Camera handling module
"""

from PyQt5.QtCore import QThread, pyqtSignal
import cv2
import time

class CameraThread(QThread):
    frame_ready = pyqtSignal(object)
    
    def __init__(self, camera_index=0):
        super().__init__()
        self.camera_index = camera_index
        self.running = False
        
    def run(self):
        """Run camera capture loop"""
        self.running = True
        cap = cv2.VideoCapture(self.camera_index)
        
        while self.running:
            ret, frame = cap.read()
            if ret:
                self.frame_ready.emit(frame)
            time.sleep(0.033)  # ~30 FPS
            
        cap.release()
        
    def stop(self):
        """Stop camera capture"""
        self.running = False
        self.wait()
