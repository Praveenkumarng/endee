"""
YOLOv9 Training Script for Cotton Leaf Disease Detection
Trains a custom YOLOv9 model on cotton disease dataset with 4 classes:
- Bacterial Blight
- Fusarium Wilt
- Healthy Leaf
- Leaf Curl Virus
"""

import os
import yaml
import torch
from ultralytics import YOLO
from pathlib import Path
import argparse
from datetime import datetime

def load_config(config_path='config/hyperparameters.yaml'):
    """Load hyperparameters from YAML configuration file"""
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config

def train_yolov9(
    data_yaml='../Leaf_Dataset/data.yaml',
    model_name='yolov9c.pt',
    epochs=100,
    batch_size=16,
    img_size=640,
    device='',
    project='runs/train',
    name='cotton_disease',
    resume=False,
    **kwargs
):
    """
    Train YOLOv9 model on cotton disease dataset
    
    Args:
        data_yaml: Path to dataset YAML configuration
        model_name: Pre-trained model to use (yolov9c.pt, yolov9e.pt, etc.)
        epochs: Number of training epochs
        batch_size: Batch size for training
        img_size: Input image size
        device: Device to use ('' for auto, '0' for GPU 0, 'cpu' for CPU)
        project: Project directory for saving results
        name: Experiment name
        resume: Resume training from last checkpoint
        **kwargs: Additional training arguments
    
    Returns:
        results: Training results
    """
    
    print("="*80)
    print("Cotton Leaf Disease Detection - YOLOv9 Training")
    print("="*80)
    print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Model: {model_name}")
    print(f"Dataset: {data_yaml}")
    print(f"Epochs: {epochs}")
    print(f"Batch Size: {batch_size}")
    print(f"Image Size: {img_size}")
    print(f"Device: {device if device else 'auto'}")
    print("="*80)
    
    # Initialize model
    model = YOLO(model_name)
    
    # Check if CUDA is available
    if torch.cuda.is_available():
        print(f"✓ CUDA Available - GPU: {torch.cuda.get_device_name(0)}")
        print(f"  GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
    else:
        print("⚠ CUDA not available - Training on CPU (will be slower)")
    
    # Training arguments
    train_args = {
        'data': data_yaml,
        'epochs': epochs,
        'batch': batch_size,
        'imgsz': img_size,
        'device': device,
        'project': project,
        'name': name,
        'exist_ok': True,
        'pretrained': True,
        'optimizer': 'AdamW',
        'verbose': True,
        'seed': 42,
        'deterministic': True,
        'val': True,
        'plots': True,
        'save': True,
        'save_period': 10,  # Save checkpoint every 10 epochs
        'cache': False,  # Set to True if you have enough RAM
        'workers': 8,
        'patience': 50,  # Early stopping patience
        'resume': resume,
        'amp': True,  # Automatic Mixed Precision
        'close_mosaic': 10,  # Disable mosaic augmentation in last N epochs
        
        # Learning rate settings
        'lr0': 0.01,  # Initial learning rate
        'lrf': 0.01,  # Final learning rate factor
        'momentum': 0.937,
        'weight_decay': 0.0005,
        'warmup_epochs': 3.0,
        'warmup_momentum': 0.8,
        'warmup_bias_lr': 0.1,
        
        # Loss weights
        'box': 7.5,  # Box loss weight
        'cls': 0.5,  # Classification loss weight
        'dfl': 1.5,  # Distribution Focal Loss weight
        
        # Data augmentation
        'hsv_h': 0.015,  # HSV-Hue augmentation
        'hsv_s': 0.7,    # HSV-Saturation augmentation
        'hsv_v': 0.4,    # HSV-Value augmentation
        'degrees': 0.0,  # Rotation (+/- deg)
        'translate': 0.1,  # Translation (+/- fraction)
        'scale': 0.5,    # Scaling (+/- gain)
        'shear': 0.0,    # Shear (+/- deg)
        'perspective': 0.0,  # Perspective (+/- fraction)
        'flipud': 0.0,   # Vertical flip probability
        'fliplr': 0.5,   # Horizontal flip probability
        'mosaic': 1.0,   # Mosaic augmentation probability
        'mixup': 0.0,    # MixUp augmentation probability
        'copy_paste': 0.0,  # Copy-paste augmentation probability
    }
    
    # Update with any additional kwargs
    train_args.update(kwargs)
    
    print("\nStarting training...")
    print("-"*80)
    
    # Train the model
    results = model.train(**train_args)
    
    print("\n" + "="*80)
    print("Training Completed!")
    print(f"End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Best weights saved to: {model.trainer.best}")
    print(f"Last weights saved to: {model.trainer.last}")
    print("="*80)
    
    return results

def main():
    """Main function to parse arguments and start training"""
    parser = argparse.ArgumentParser(description='Train YOLOv9 on Cotton Disease Dataset')
    
    parser.add_argument('--data', type=str, default='../Leaf_Dataset/data.yaml',
                        help='Path to dataset YAML file')
    parser.add_argument('--model', type=str, default='yolov9c.pt',
                        help='Model to use (yolov9c.pt, yolov9e.pt, etc.)')
    parser.add_argument('--epochs', type=int, default=100,
                        help='Number of training epochs')
    parser.add_argument('--batch', type=int, default=16,
                        help='Batch size')
    parser.add_argument('--imgsz', type=int, default=640,
                        help='Input image size')
    parser.add_argument('--device', type=str, default='',
                        help='Device to use (empty for auto, 0 for GPU, cpu for CPU)')
    parser.add_argument('--project', type=str, default='runs/train',
                        help='Project directory')
    parser.add_argument('--name', type=str, default='cotton_disease',
                        help='Experiment name')
    parser.add_argument('--resume', action='store_true',
                        help='Resume training from last checkpoint')
    parser.add_argument('--config', type=str, default=None,
                        help='Path to hyperparameters config file')
    
    args = parser.parse_args()
    
    # Load config if provided
    if args.config and os.path.exists(args.config):
        config = load_config(args.config)
        # Override with config values
        for key, value in config.items():
            if hasattr(args, key):
                setattr(args, key, value)
    
    # Start training
    train_yolov9(
        data_yaml=args.data,
        model_name=args.model,
        epochs=args.epochs,
        batch_size=args.batch,
        img_size=args.imgsz,
        device=args.device,
        project=args.project,
        name=args.name,
        resume=args.resume
    )

if __name__ == '__main__':
    main()
