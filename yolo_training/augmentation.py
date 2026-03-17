"""
Data Augmentation Pipeline for Cotton Leaf Disease Detection
Uses Albumentations library for advanced augmentation techniques
"""

import albumentations as A
from albumentations.pytorch import ToTensorV2
import cv2
import numpy as np
import os
from pathlib import Path
import yaml

class CottonDiseaseAugmentation:
    """
    Custom augmentation pipeline for cotton leaf disease images
    Preserves YOLO bounding box format
    """
    
    def __init__(self, img_size=640, augment=True):
        """
        Initialize augmentation pipeline
        
        Args:
            img_size: Target image size
            augment: Whether to apply augmentation
        """
        self.img_size = img_size
        self.augment = augment
        
        if augment:
            self.transform = A.Compose([
                # Geometric transformations
                A.HorizontalFlip(p=0.5),
                A.VerticalFlip(p=0.2),
                A.RandomRotate90(p=0.3),
                A.ShiftScaleRotate(
                    shift_limit=0.1,
                    scale_limit=0.2,
                    rotate_limit=15,
                    border_mode=cv2.BORDER_CONSTANT,
                    p=0.5
                ),
                
                # Color augmentations
                A.OneOf([
                    A.HueSaturationValue(
                        hue_shift_limit=20,
                        sat_shift_limit=30,
                        val_shift_limit=20,
                        p=1.0
                    ),
                    A.RGBShift(
                        r_shift_limit=20,
                        g_shift_limit=20,
                        b_shift_limit=20,
                        p=1.0
                    ),
                    A.ColorJitter(
                        brightness=0.2,
                        contrast=0.2,
                        saturation=0.2,
                        hue=0.1,
                        p=1.0
                    ),
                ], p=0.7),
                
                # Brightness and contrast
                A.RandomBrightnessContrast(
                    brightness_limit=0.2,
                    contrast_limit=0.2,
                    p=0.5
                ),
                
                # Blur and noise
                A.OneOf([
                    A.GaussianBlur(blur_limit=(3, 5), p=1.0),
                    A.MedianBlur(blur_limit=5, p=1.0),
                    A.MotionBlur(blur_limit=5, p=1.0),
                ], p=0.3),
                
                A.GaussNoise(var_limit=(10.0, 50.0), p=0.2),
                
                # Weather effects (simulating field conditions)
                A.OneOf([
                    A.RandomRain(
                        slant_lower=-10,
                        slant_upper=10,
                        drop_length=20,
                        drop_width=1,
                        drop_color=(200, 200, 200),
                        blur_value=3,
                        brightness_coefficient=0.9,
                        rain_type=None,
                        p=1.0
                    ),
                    A.RandomSunFlare(
                        flare_roi=(0, 0, 1, 0.5),
                        angle_lower=0,
                        angle_upper=1,
                        num_flare_circles_lower=1,
                        num_flare_circles_upper=2,
                        src_radius=100,
                        src_color=(255, 255, 255),
                        p=1.0
                    ),
                ], p=0.1),
                
                # Resize to target size
                A.Resize(height=img_size, width=img_size, p=1.0),
                
            ], bbox_params=A.BboxParams(
                format='yolo',
                label_fields=['class_labels'],
                min_visibility=0.3
            ))
        else:
            # No augmentation, just resize
            self.transform = A.Compose([
                A.Resize(height=img_size, width=img_size, p=1.0),
            ], bbox_params=A.BboxParams(
                format='yolo',
                label_fields=['class_labels']
            ))
    
    def __call__(self, image, bboxes, class_labels):
        """
        Apply augmentation to image and bounding boxes
        
        Args:
            image: Input image (numpy array)
            bboxes: List of bounding boxes in YOLO format [x_center, y_center, width, height]
            class_labels: List of class labels for each bbox
        
        Returns:
            transformed: Dictionary with augmented image and bboxes
        """
        transformed = self.transform(
            image=image,
            bboxes=bboxes,
            class_labels=class_labels
        )
        
        return transformed

def load_yolo_annotation(label_path):
    """
    Load YOLO format annotation file
    
    Args:
        label_path: Path to .txt annotation file
    
    Returns:
        bboxes: List of bounding boxes
        class_labels: List of class labels
    """
    bboxes = []
    class_labels = []
    
    if os.path.exists(label_path):
        with open(label_path, 'r') as f:
            for line in f.readlines():
                parts = line.strip().split()
                if len(parts) == 5:
                    class_id = int(parts[0])
                    bbox = [float(x) for x in parts[1:]]
                    class_labels.append(class_id)
                    bboxes.append(bbox)
    
    return bboxes, class_labels

def save_yolo_annotation(label_path, bboxes, class_labels):
    """
    Save YOLO format annotation file
    
    Args:
        label_path: Path to save .txt annotation file
        bboxes: List of bounding boxes
        class_labels: List of class labels
    """
    with open(label_path, 'w') as f:
        for bbox, class_id in zip(bboxes, class_labels):
            line = f"{class_id} {' '.join([str(x) for x in bbox])}\n"
            f.write(line)

def augment_dataset(
    input_dir,
    output_dir,
    num_augmentations=3,
    img_size=640
):
    """
    Augment entire dataset
    
    Args:
        input_dir: Input directory containing images/ and labels/
        output_dir: Output directory for augmented data
        num_augmentations: Number of augmented versions per image
        img_size: Target image size
    """
    
    print(f"Augmenting dataset from {input_dir}")
    print(f"Output directory: {output_dir}")
    print(f"Augmentations per image: {num_augmentations}")
    
    # Create output directories
    os.makedirs(os.path.join(output_dir, 'images'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'labels'), exist_ok=True)
    
    # Initialize augmentation pipeline
    augmentor = CottonDiseaseAugmentation(img_size=img_size, augment=True)
    
    # Get all images
    image_dir = os.path.join(input_dir, 'images')
    label_dir = os.path.join(input_dir, 'labels')
    
    image_files = [f for f in os.listdir(image_dir) if f.endswith(('.jpg', '.png', '.jpeg'))]
    
    total_images = len(image_files)
    print(f"Found {total_images} images")
    
    for idx, img_file in enumerate(image_files):
        # Load image
        img_path = os.path.join(image_dir, img_file)
        image = cv2.imread(img_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Load annotations
        label_file = os.path.splitext(img_file)[0] + '.txt'
        label_path = os.path.join(label_dir, label_file)
        bboxes, class_labels = load_yolo_annotation(label_path)
        
        # Save original
        output_img_path = os.path.join(output_dir, 'images', img_file)
        output_label_path = os.path.join(output_dir, 'labels', label_file)
        cv2.imwrite(output_img_path, cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
        save_yolo_annotation(output_label_path, bboxes, class_labels)
        
        # Generate augmented versions
        for aug_idx in range(num_augmentations):
            try:
                # Apply augmentation
                transformed = augmentor(image, bboxes, class_labels)
                
                # Save augmented image
                aug_img_name = f"{os.path.splitext(img_file)[0]}_aug{aug_idx}{os.path.splitext(img_file)[1]}"
                aug_label_name = f"{os.path.splitext(img_file)[0]}_aug{aug_idx}.txt"
                
                aug_img_path = os.path.join(output_dir, 'images', aug_img_name)
                aug_label_path = os.path.join(output_dir, 'labels', aug_label_name)
                
                cv2.imwrite(aug_img_path, cv2.cvtColor(transformed['image'], cv2.COLOR_RGB2BGR))
                save_yolo_annotation(aug_label_path, transformed['bboxes'], transformed['class_labels'])
                
            except Exception as e:
                print(f"Error augmenting {img_file}: {str(e)}")
        
        if (idx + 1) % 100 == 0:
            print(f"Processed {idx + 1}/{total_images} images")
    
    print(f"\nAugmentation complete!")
    print(f"Total images generated: {total_images * (num_augmentations + 1)}")

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Augment Cotton Disease Dataset')
    parser.add_argument('--input', type=str, required=True,
                        help='Input directory (containing images/ and labels/)')
    parser.add_argument('--output', type=str, required=True,
                        help='Output directory for augmented data')
    parser.add_argument('--num-aug', type=int, default=3,
                        help='Number of augmentations per image')
    parser.add_argument('--imgsz', type=int, default=640,
                        help='Target image size')
    
    args = parser.parse_args()
    
    augment_dataset(
        input_dir=args.input,
        output_dir=args.output,
        num_augmentations=args.num_aug,
        img_size=args.imgsz
    )
