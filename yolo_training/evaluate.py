"""
YOLOv9 Model Evaluation Script
Evaluates trained model on test set and generates performance metrics
"""

import os
import yaml
import torch
from ultralytics import YOLO
from pathlib import Path
import argparse
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.metrics import confusion_matrix, classification_report
import json
from datetime import datetime

def evaluate_model(
    weights_path,
    data_yaml='../Leaf_Dataset/data.yaml',
    img_size=640,
    batch_size=16,
    device='',
    save_dir='runs/evaluate',
    conf_threshold=0.25,
    iou_threshold=0.7
):
    """
    Evaluate YOLOv9 model on test dataset
    
    Args:
        weights_path: Path to trained model weights (.pt file)
        data_yaml: Path to dataset YAML configuration
        img_size: Input image size
        batch_size: Batch size for evaluation
        device: Device to use
        save_dir: Directory to save evaluation results
        conf_threshold: Confidence threshold for predictions
        iou_threshold: IOU threshold for NMS
    
    Returns:
        metrics: Dictionary containing evaluation metrics
    """
    
    print("="*80)
    print("Cotton Leaf Disease Detection - Model Evaluation")
    print("="*80)
    print(f"Evaluation Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Model Weights: {weights_path}")
    print(f"Dataset: {data_yaml}")
    print("="*80)
    
    # Create save directory
    os.makedirs(save_dir, exist_ok=True)
    
    # Load model
    print("\nLoading model...")
    model = YOLO(weights_path)
    
    # Check device
    if torch.cuda.is_available():
        print(f"✓ Using GPU: {torch.cuda.get_device_name(0)}")
    else:
        print("⚠ Using CPU")
    
    # Validate on test set
    print("\nRunning validation on test set...")
    print("-"*80)
    
    results = model.val(
        data=data_yaml,
        split='test',
        imgsz=img_size,
        batch=batch_size,
        device=device,
        conf=conf_threshold,
        iou=iou_threshold,
        plots=True,
        save_json=True,
        project=save_dir,
        name='test_results'
    )
    
    # Extract metrics
    metrics = {
        'mAP50': float(results.box.map50),  # mAP@0.5
        'mAP50-95': float(results.box.map),  # mAP@0.5:0.95
        'precision': float(results.box.mp),  # Mean precision
        'recall': float(results.box.mr),     # Mean recall
        'f1_score': 2 * (float(results.box.mp) * float(results.box.mr)) / (float(results.box.mp) + float(results.box.mr) + 1e-6)
    }
    
    # Per-class metrics
    class_names = ['Bacterial Blight', 'Fusarium Wilt', 'Healthy Leaf', 'Leaf Curl Virus']
    
    print("\n" + "="*80)
    print("EVALUATION RESULTS")
    print("="*80)
    print(f"\nOverall Metrics:")
    print(f"  mAP@0.5:     {metrics['mAP50']:.4f} ({metrics['mAP50']*100:.2f}%)")
    print(f"  mAP@0.5:0.95: {metrics['mAP50-95']:.4f} ({metrics['mAP50-95']*100:.2f}%)")
    print(f"  Precision:   {metrics['precision']:.4f} ({metrics['precision']*100:.2f}%)")
    print(f"  Recall:      {metrics['recall']:.4f} ({metrics['recall']*100:.2f}%)")
    print(f"  F1-Score:    {metrics['f1_score']:.4f} ({metrics['f1_score']*100:.2f}%)")
    
    # Check if mAP > 90%
    if metrics['mAP50'] > 0.90:
        print(f"\n✓ SUCCESS: Model achieves >90% mAP@0.5!")
    else:
        print(f"\n⚠ WARNING: Model mAP@0.5 is {metrics['mAP50']*100:.2f}%, below 90% target")
    
    # Per-class metrics
    if hasattr(results.box, 'ap_class_index'):
        print(f"\nPer-Class Metrics:")
        print("-"*80)
        print(f"{'Class':<20} {'Precision':<12} {'Recall':<12} {'mAP@0.5':<12}")
        print("-"*80)
        
        for i, class_idx in enumerate(results.box.ap_class_index):
            class_name = class_names[int(class_idx)]
            precision = results.box.p[i] if hasattr(results.box, 'p') else 0
            recall = results.box.r[i] if hasattr(results.box, 'r') else 0
            ap = results.box.ap50[i] if hasattr(results.box, 'ap50') else 0
            
            print(f"{class_name:<20} {precision:<12.4f} {recall:<12.4f} {ap:<12.4f}")
    
    print("="*80)
    
    # Save metrics to JSON
    metrics_file = os.path.join(save_dir, 'test_results', 'metrics.json')
    with open(metrics_file, 'w') as f:
        json.dump(metrics, f, indent=4)
    
    print(f"\n✓ Metrics saved to: {metrics_file}")
    print(f"✓ Plots saved to: {os.path.join(save_dir, 'test_results')}")
    
    return metrics

def benchmark_inference_speed(weights_path, img_size=640, device='', num_iterations=100):
    """
    Benchmark inference speed to verify >30 FPS requirement
    
    Args:
        weights_path: Path to model weights
        img_size: Input image size
        device: Device to use
        num_iterations: Number of iterations for benchmarking
    
    Returns:
        fps: Frames per second
    """
    
    print("\n" + "="*80)
    print("INFERENCE SPEED BENCHMARK")
    print("="*80)
    
    # Load model
    model = YOLO(weights_path)
    
    # Create dummy input
    dummy_input = torch.randn(1, 3, img_size, img_size)
    
    if device and device != 'cpu':
        dummy_input = dummy_input.cuda()
        model.model = model.model.cuda()
    
    # Warmup
    print("Warming up...")
    for _ in range(10):
        _ = model.predict(dummy_input, verbose=False)
    
    # Benchmark
    print(f"Running {num_iterations} iterations...")
    
    if torch.cuda.is_available():
        torch.cuda.synchronize()
    
    import time
    start_time = time.time()
    
    for _ in range(num_iterations):
        _ = model.predict(dummy_input, verbose=False)
    
    if torch.cuda.is_available():
        torch.cuda.synchronize()
    
    end_time = time.time()
    
    # Calculate FPS
    total_time = end_time - start_time
    fps = num_iterations / total_time
    avg_inference_time = (total_time / num_iterations) * 1000  # in ms
    
    print(f"\nResults:")
    print(f"  Total Time:       {total_time:.2f} seconds")
    print(f"  Average Time:     {avg_inference_time:.2f} ms/image")
    print(f"  Throughput:       {fps:.2f} FPS")
    
    if fps > 30:
        print(f"\n✓ SUCCESS: Model achieves >30 FPS!")
    else:
        print(f"\n⚠ WARNING: Model FPS is {fps:.2f}, below 30 FPS target")
    
    print("="*80)
    
    return fps

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Evaluate YOLOv9 Cotton Disease Model')
    
    parser.add_argument('--weights', type=str, required=True,
                        help='Path to model weights (.pt file)')
    parser.add_argument('--data', type=str, default='../Leaf_Dataset/data.yaml',
                        help='Path to dataset YAML file')
    parser.add_argument('--imgsz', type=int, default=640,
                        help='Input image size')
    parser.add_argument('--batch', type=int, default=16,
                        help='Batch size')
    parser.add_argument('--device', type=str, default='',
                        help='Device to use')
    parser.add_argument('--save-dir', type=str, default='runs/evaluate',
                        help='Directory to save results')
    parser.add_argument('--conf', type=float, default=0.25,
                        help='Confidence threshold')
    parser.add_argument('--iou', type=float, default=0.7,
                        help='IOU threshold for NMS')
    parser.add_argument('--benchmark', action='store_true',
                        help='Run inference speed benchmark')
    
    args = parser.parse_args()
    
    # Evaluate model
    metrics = evaluate_model(
        weights_path=args.weights,
        data_yaml=args.data,
        img_size=args.imgsz,
        batch_size=args.batch,
        device=args.device,
        save_dir=args.save_dir,
        conf_threshold=args.conf,
        iou_threshold=args.iou
    )
    
    # Benchmark if requested
    if args.benchmark:
        fps = benchmark_inference_speed(
            weights_path=args.weights,
            img_size=args.imgsz,
            device=args.device
        )

if __name__ == '__main__':
    main()
