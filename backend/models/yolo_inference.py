"""
YOLOv9 Inference Module
Handles model loading and inference for cotton disease detection
"""

import cv2
import numpy as np
import torch
from ultralytics import YOLO
import time
from typing import List, Dict, Tuple
import io
from PIL import Image

class YOLOInference:
    """
    YOLOv9 inference wrapper for cotton leaf disease detection
    """
    
    def __init__(self, weights_path: str, device: str = ''):
        """
        Initialize YOLO model
        
        Args:
            weights_path: Path to model weights (.pt or .onnx)
            device: Device to use ('' for auto, 'cpu', '0' for GPU 0)
        """
        
        self.weights_path = weights_path
        self.device = device
        
        # Class names for cotton diseases
        self.class_names = [
            'Bacterial Blight',
            'Fusarium Wilt',
            'Healthy Leaf',
            'Leaf Curl Virus'
        ]
        
        # Load model
        print(f"Loading model from: {weights_path}")
        self.model = YOLO(weights_path)
        
        # Set device
        if device:
            self.model.to(device)
        
        # Check if CUDA is available
        self.use_cuda = torch.cuda.is_available() and device != 'cpu'
        
        if self.use_cuda:
            print(f"✓ Using GPU: {torch.cuda.get_device_name(0)}")
        else:
            print("✓ Using CPU")
        
        print("✓ Model loaded successfully")
    
    def preprocess_image(self, image_bytes: bytes) -> np.ndarray:
        """
        Preprocess image from bytes
        
        Args:
            image_bytes: Raw image bytes
        
        Returns:
            image: Preprocessed image as numpy array
        """
        
        # Convert bytes to PIL Image
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Convert to numpy array
        image = np.array(image)
        
        # Convert RGB to BGR for OpenCV compatibility
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        return image
    
    def postprocess_results(
        self,
        results,
        image_shape: Tuple[int, int],
        conf_threshold: float = 0.25
    ) -> List[Dict]:
        """
        Post-process YOLO results
        
        Args:
            results: YOLO results object
            image_shape: Original image shape (height, width)
            conf_threshold: Confidence threshold
        
        Returns:
            detections: List of detection dictionaries
        """
        
        detections = []
        
        # Extract results
        for result in results:
            boxes = result.boxes
            
            if boxes is None or len(boxes) == 0:
                continue
            
            # Process each detection
            for box in boxes:
                # Get box coordinates
                xyxy = box.xyxy[0].cpu().numpy()  # [x1, y1, x2, y2]
                conf = float(box.conf[0].cpu().numpy())
                cls = int(box.cls[0].cpu().numpy())
                
                # Filter by confidence
                if conf < conf_threshold:
                    continue
                
                # Normalize coordinates
                h, w = image_shape
                x1_norm = float(xyxy[0] / w)
                y1_norm = float(xyxy[1] / h)
                x2_norm = float(xyxy[2] / w)
                y2_norm = float(xyxy[3] / h)
                
                # Create detection dict
                detection = {
                    'class_id': cls,
                    'class_name': self.class_names[cls],
                    'confidence': conf,
                    'bbox': [float(xyxy[0]), float(xyxy[1]), float(xyxy[2]), float(xyxy[3])],
                    'bbox_normalized': [x1_norm, y1_norm, x2_norm, y2_norm]
                }
                
                detections.append(detection)
        
        return detections
    
    def predict(
        self,
        image_bytes: bytes,
        conf_threshold: float = 0.25,
        iou_threshold: float = 0.7
    ) -> Dict:
        """
        Run inference on image
        
        Args:
            image_bytes: Raw image bytes
            conf_threshold: Confidence threshold for detections
            iou_threshold: IOU threshold for NMS
        
        Returns:
            results: Dictionary containing detections and metadata
        """
        
        # Preprocess image
        image = self.preprocess_image(image_bytes)
        image_shape = image.shape[:2]  # (height, width)
        
        # Run inference
        start_time = time.time()
        
        results = self.model.predict(
            image,
            conf=conf_threshold,
            iou=iou_threshold,
            verbose=False,
            device=self.device
        )
        
        end_time = time.time()
        inference_time_ms = (end_time - start_time) * 1000
        
        # Post-process results
        detections = self.postprocess_results(results, image_shape, conf_threshold)
        
        return {
            'detections': detections,
            'image_shape': image_shape,
            'inference_time_ms': inference_time_ms,
            'num_detections': len(detections)
        }
    
    def predict_batch(
        self,
        images: List[bytes],
        conf_threshold: float = 0.25,
        iou_threshold: float = 0.7
    ) -> List[Dict]:
        """
        Run inference on batch of images
        
        Args:
            images: List of image bytes
            conf_threshold: Confidence threshold
            iou_threshold: IOU threshold
        
        Returns:
            results: List of result dictionaries
        """
        
        results = []
        
        for image_bytes in images:
            result = self.predict(image_bytes, conf_threshold, iou_threshold)
            results.append(result)
        
        return results
    
    def get_fps(self, num_iterations: int = 100) -> float:
        """
        Benchmark inference speed
        
        Args:
            num_iterations: Number of iterations for benchmarking
        
        Returns:
            fps: Frames per second
        """
        
        # Create dummy input
        dummy_image = np.random.randint(0, 255, (640, 640, 3), dtype=np.uint8)
        
        # Warmup
        for _ in range(10):
            _ = self.model.predict(dummy_image, verbose=False)
        
        # Benchmark
        if self.use_cuda:
            torch.cuda.synchronize()
        
        start_time = time.time()
        
        for _ in range(num_iterations):
            _ = self.model.predict(dummy_image, verbose=False)
        
        if self.use_cuda:
            torch.cuda.synchronize()
        
        end_time = time.time()
        
        # Calculate FPS
        total_time = end_time - start_time
        fps = num_iterations / total_time
        
        return fps

class ONNXInference:
    """
    ONNX Runtime inference for optimized deployment
    """
    
    def __init__(self, onnx_path: str, use_gpu: bool = False):
        """
        Initialize ONNX model
        
        Args:
            onnx_path: Path to ONNX model
            use_gpu: Whether to use GPU acceleration
        """
        
        import onnxruntime as ort
        
        self.onnx_path = onnx_path
        
        # Class names
        self.class_names = [
            'Bacterial Blight',
            'Fusarium Wilt',
            'Healthy Leaf',
            'Leaf Curl Virus'
        ]
        
        # Set providers
        providers = ['CUDAExecutionProvider', 'CPUExecutionProvider'] if use_gpu else ['CPUExecutionProvider']
        
        # Create session
        self.session = ort.InferenceSession(onnx_path, providers=providers)
        
        # Get input/output names
        self.input_name = self.session.get_inputs()[0].name
        self.output_names = [output.name for output in self.session.get_outputs()]
        
        print(f"✓ ONNX model loaded from: {onnx_path}")
        print(f"  Providers: {self.session.get_providers()}")
    
    def predict(self, image_bytes: bytes, conf_threshold: float = 0.25) -> Dict:
        """
        Run ONNX inference
        
        Args:
            image_bytes: Raw image bytes
            conf_threshold: Confidence threshold
        
        Returns:
            results: Detection results
        """
        
        # Preprocess image
        image = Image.open(io.BytesIO(image_bytes))
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        image = np.array(image)
        image = cv2.resize(image, (640, 640))
        
        # Normalize and transpose
        image = image.transpose(2, 0, 1)  # HWC to CHW
        image = np.expand_dims(image, axis=0)  # Add batch dimension
        image = image.astype(np.float32) / 255.0
        
        # Run inference
        start_time = time.time()
        outputs = self.session.run(self.output_names, {self.input_name: image})
        end_time = time.time()
        
        inference_time_ms = (end_time - start_time) * 1000
        
        # Post-process outputs
        # Note: ONNX output format may vary, adjust as needed
        detections = []
        
        return {
            'detections': detections,
            'inference_time_ms': inference_time_ms
        }
