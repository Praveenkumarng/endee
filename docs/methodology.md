# Methodology

## Dataset Preparation

### Dataset Source
- **Source**: Roboflow Universe
- **Total Images**: 1257
- **Format**: YOLOv9
- **Classes**: 4 (Bacterial Blight, Fusarium Wilt, Healthy Leaf, Leaf Curl Virus)

### Dataset Split
- **Training**: 890 images (70.8%)
- **Validation**: 252 images (20.0%)
- **Testing**: 115 images (9.2%)

### Preprocessing
- Auto-orientation correction
- Resize to 640x640 (stretch)
- YOLO format annotations

### Augmentation (Training)
- Horizontal flip (50%)
- HSV color jitter
- Random brightness/contrast
- Mosaic augmentation
- MixUp augmentation

## Model Selection

### Why YOLOv9?
1. **State-of-the-art accuracy**: Latest YOLO version
2. **Real-time performance**: >30 FPS on GPU
3. **Single-stage detector**: Efficient inference
4. **Strong backbone**: Better feature extraction
5. **Active development**: Regular updates

### Model Variant
- **Selected**: YOLOv9c (compact)
- **Rationale**: Balance between speed and accuracy
- **Parameters**: ~25M
- **FLOPs**: ~102G

## Training Strategy

### Hyperparameters
- **Epochs**: 100
- **Batch Size**: 16
- **Image Size**: 640x640
- **Optimizer**: AdamW
- **Learning Rate**: 0.01 (initial), 0.0001 (final)
- **Weight Decay**: 0.0005
- **Momentum**: 0.937

### Loss Function
- **Box Loss**: IoU-based
- **Classification Loss**: Binary cross-entropy
- **DFL Loss**: Distribution focal loss

### Training Techniques
1. **Transfer Learning**: Pre-trained on COCO
2. **Data Augmentation**: Extensive augmentation pipeline
3. **Early Stopping**: Patience of 50 epochs
4. **Learning Rate Scheduling**: Cosine annealing
5. **Mixed Precision**: FP16 training for speed

## Evaluation Metrics

### Primary Metrics
1. **mAP@0.5**: Mean Average Precision at IoU 0.5
2. **mAP@0.5:0.95**: mAP across IoU thresholds
3. **Precision**: True positives / (True positives + False positives)
4. **Recall**: True positives / (True positives + False negatives)
5. **F1-Score**: Harmonic mean of precision and recall

### Performance Metrics
1. **Inference Time**: Time per image (ms)
2. **FPS**: Frames per second
3. **Model Size**: File size in MB

## Severity Analysis Algorithm

```python
def calculate_severity(detections, image_area):
    infected_area = sum(bbox_area for det in detections if det.class != "Healthy")
    percentage = (infected_area / image_area) * 100
    
    if percentage < 10:
        return "Mild"
    elif percentage < 30:
        return "Moderate"
    else:
        return "Severe"
```

## Recommendation System

### Decision Logic
1. Identify detected diseases
2. Determine severity level
3. Select appropriate treatments:
   - **Severe**: Chemical + Organic + Prevention
   - **Moderate**: Organic + Prevention
   - **Mild**: Prevention only
4. Prioritize by effectiveness and severity

### Treatment Categories
1. **Chemical**: Fungicides, bactericides, insecticides
2. **Organic**: Biocontrol agents, natural remedies
3. **Prevention**: Cultural practices, resistant varieties

## Performance Optimization

### Model Optimization
1. **Quantization**: FP16 for faster inference
2. **ONNX Export**: Cross-platform deployment
3. **TensorRT**: GPU optimization (optional)

### Code Optimization
1. **Batch Processing**: Process multiple images
2. **Async API**: Non-blocking requests
3. **Caching**: Model loaded once
4. **GPU Acceleration**: CUDA when available

## Validation Strategy

### Cross-Validation
- 5-fold cross-validation on training set
- Ensures model generalization

### Test Set Evaluation
- Held-out test set (115 images)
- Never used during training
- Final performance metric

### Real-World Testing
- Field testing with actual cotton plants
- Various lighting conditions
- Different camera angles
- Multiple growth stages

## Future Improvements

1. **Larger Dataset**: Collect more diverse samples
2. **Additional Classes**: More disease types
3. **Multi-Stage Detection**: Detect disease progression
4. **Ensemble Models**: Combine multiple models
5. **Active Learning**: Continuous improvement
6. **Edge Deployment**: Mobile and IoT devices
