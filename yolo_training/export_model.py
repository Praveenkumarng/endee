"""
Export YOLOv9 Model to Multiple Formats
Exports trained model to .pt and ONNX formats for deployment
"""

import os
import argparse
from ultralytics import YOLO
import torch
from datetime import datetime

def export_model(
    weights_path,
    formats=['onnx', 'torchscript'],
    img_size=640,
    device='cpu',
    simplify=True,
    dynamic=False,
    half=False
):
    """
    Export YOLOv9 model to various formats
    
    Args:
        weights_path: Path to trained model weights (.pt file)
        formats: List of export formats ('onnx', 'torchscript', 'engine', etc.)
        img_size: Input image size
        device: Device to use for export
        simplify: Simplify ONNX model
        dynamic: Dynamic input shapes for ONNX
        half: FP16 half-precision export
    
    Returns:
        export_paths: Dictionary of exported model paths
    """
    
    print("="*80)
    print("Cotton Leaf Disease Detection - Model Export")
    print("="*80)
    print(f"Export Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Model Weights: {weights_path}")
    print(f"Export Formats: {', '.join(formats)}")
    print(f"Image Size: {img_size}")
    print("="*80)
    
    # Load model
    print("\nLoading model...")
    model = YOLO(weights_path)
    
    export_paths = {}
    
    # Export to each format
    for fmt in formats:
        print(f"\n{'='*80}")
        print(f"Exporting to {fmt.upper()}...")
        print(f"{'='*80}")
        
        try:
            if fmt == 'onnx':
                # Export to ONNX
                export_path = model.export(
                    format='onnx',
                    imgsz=img_size,
                    device=device,
                    simplify=simplify,
                    dynamic=dynamic,
                    half=half,
                    opset=12  # ONNX opset version
                )
                export_paths['onnx'] = export_path
                print(f"✓ ONNX export successful: {export_path}")
                
                # Verify ONNX model
                print("\nVerifying ONNX model...")
                import onnx
                onnx_model = onnx.load(export_path)
                onnx.checker.check_model(onnx_model)
                print("✓ ONNX model verification passed")
                
            elif fmt == 'torchscript':
                # Export to TorchScript
                export_path = model.export(
                    format='torchscript',
                    imgsz=img_size,
                    device=device
                )
                export_paths['torchscript'] = export_path
                print(f"✓ TorchScript export successful: {export_path}")
                
            elif fmt == 'engine':
                # Export to TensorRT (requires TensorRT installed)
                export_path = model.export(
                    format='engine',
                    imgsz=img_size,
                    device=device,
                    half=half
                )
                export_paths['engine'] = export_path
                print(f"✓ TensorRT export successful: {export_path}")
                
            elif fmt == 'coreml':
                # Export to CoreML (for iOS/macOS)
                export_path = model.export(
                    format='coreml',
                    imgsz=img_size
                )
                export_paths['coreml'] = export_path
                print(f"✓ CoreML export successful: {export_path}")
                
            else:
                print(f"⚠ Unknown format: {fmt}")
                
        except Exception as e:
            print(f"✗ Export to {fmt} failed: {str(e)}")
    
    print("\n" + "="*80)
    print("EXPORT SUMMARY")
    print("="*80)
    print(f"\nSuccessfully exported to {len(export_paths)} format(s):")
    for fmt, path in export_paths.items():
        file_size = os.path.getsize(path) / (1024 * 1024)  # Size in MB
        print(f"  {fmt.upper():<15} {path}")
        print(f"  {'Size:':<15} {file_size:.2f} MB")
    
    print("="*80)
    
    return export_paths

def test_exported_model(onnx_path, test_image=None, img_size=640):
    """
    Test exported ONNX model with a sample inference
    
    Args:
        onnx_path: Path to exported ONNX model
        test_image: Path to test image (optional)
        img_size: Input image size
    """
    
    print("\n" + "="*80)
    print("TESTING EXPORTED ONNX MODEL")
    print("="*80)
    
    try:
        import onnxruntime as ort
        import numpy as np
        from PIL import Image
        import cv2
        
        # Create ONNX Runtime session
        print(f"\nLoading ONNX model: {onnx_path}")
        session = ort.InferenceSession(onnx_path, providers=['CPUExecutionProvider'])
        
        # Get input/output names
        input_name = session.get_inputs()[0].name
        output_names = [output.name for output in session.get_outputs()]
        
        print(f"✓ Model loaded successfully")
        print(f"  Input name: {input_name}")
        print(f"  Output names: {output_names}")
        
        # Create dummy input or use test image
        if test_image and os.path.exists(test_image):
            print(f"\nUsing test image: {test_image}")
            img = cv2.imread(test_image)
            img = cv2.resize(img, (img_size, img_size))
            img = img.transpose(2, 0, 1)  # HWC to CHW
            img = np.expand_dims(img, axis=0)  # Add batch dimension
            img = img.astype(np.float32) / 255.0  # Normalize
        else:
            print("\nUsing dummy input")
            img = np.random.randn(1, 3, img_size, img_size).astype(np.float32)
        
        # Run inference
        print("Running inference...")
        import time
        start = time.time()
        outputs = session.run(output_names, {input_name: img})
        end = time.time()
        
        inference_time = (end - start) * 1000  # Convert to ms
        
        print(f"✓ Inference successful")
        print(f"  Inference time: {inference_time:.2f} ms")
        print(f"  Output shape: {outputs[0].shape}")
        
        print("="*80)
        
    except ImportError:
        print("⚠ onnxruntime not installed. Skipping ONNX model test.")
        print("  Install with: pip install onnxruntime")
    except Exception as e:
        print(f"✗ ONNX model test failed: {str(e)}")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Export YOLOv9 Cotton Disease Model')
    
    parser.add_argument('--weights', type=str, required=True,
                        help='Path to model weights (.pt file)')
    parser.add_argument('--formats', nargs='+', default=['onnx', 'torchscript'],
                        help='Export formats (onnx, torchscript, engine, coreml)')
    parser.add_argument('--imgsz', type=int, default=640,
                        help='Input image size')
    parser.add_argument('--device', type=str, default='cpu',
                        help='Device to use for export')
    parser.add_argument('--simplify', action='store_true', default=True,
                        help='Simplify ONNX model')
    parser.add_argument('--dynamic', action='store_true',
                        help='Dynamic input shapes for ONNX')
    parser.add_argument('--half', action='store_true',
                        help='FP16 half-precision export')
    parser.add_argument('--test', action='store_true',
                        help='Test exported ONNX model')
    parser.add_argument('--test-image', type=str, default=None,
                        help='Test image path for ONNX testing')
    
    args = parser.parse_args()
    
    # Export model
    export_paths = export_model(
        weights_path=args.weights,
        formats=args.formats,
        img_size=args.imgsz,
        device=args.device,
        simplify=args.simplify,
        dynamic=args.dynamic,
        half=args.half
    )
    
    # Test ONNX model if requested
    if args.test and 'onnx' in export_paths:
        test_exported_model(
            onnx_path=export_paths['onnx'],
            test_image=args.test_image,
            img_size=args.imgsz
        )

if __name__ == '__main__':
    main()
