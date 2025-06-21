"""
generate.py - YOLOv8 Detection and Visualization Generator

This module provides functionality to run YOLOv8 object detection on a set of images
and generate various visualization outputs. Features include:

- Batch processing of multiple image formats
- Generation of detection overlays with bounding boxes
- Creation of binary detection masks
- Export of detection results in text format
- GUI-based configuration
- Progress tracking with tqdm
- Comprehensive error handling
"""

from ultralytics import YOLO
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from tqdm import tqdm
import cv2
import numpy as np
from scripts.utils.ui.form import FormGenerator
from scripts.utils.ui.popup import PopupManager
from scripts.utils.ui.input import Input
from typing import Dict, Any

def run_generation(args: Dict[str, Any]) -> bool:
    """
    Execute YOLOv8 detection and generate visualization outputs.

    This function:
    1. Sets up output directories for different visualization types
    2. Loads and configures the YOLO model
    3. Processes all images in the input directory
    4. Generates overlays with bounding boxes and labels
    5. Creates binary masks for detected objects
    6. Saves detection data in text format

    Args:
        args: Configuration dictionary containing:
            - model_path: Path to YOLOv8 model file
            - input_dir: Directory containing images to process
            - output_dir: Directory for saving outputs
            - font_size: Size of label text in overlays

    Returns:
        bool: True if processing completed successfully, False otherwise
    """
    popup = PopupManager()
    try:
        # Setup output directory structure
        input_dir = Path(args['input_dir'])
        output_dir = Path(args['output_dir'])
        overlay_dir = output_dir / 'overlays'  # For annotated images
        detection_dir = output_dir / 'detections'  # For text results
        mask_dir = output_dir / 'masks'  # For binary masks

        # Create output directories if they don't exist
        for dir in [overlay_dir, detection_dir, mask_dir]:
            dir.mkdir(parents=True, exist_ok=True)

        # Initialize model and font
        model = YOLO(args['model_path'])
        try:
            font = ImageFont.load_default(size=args['font_size'])
        except:
            font = ImageFont.load_default()

        # Collect all supported image files
        image_paths = []
        for ext in ['*.jpg', '*.jpeg', '*.png']:
            image_paths.extend(input_dir.glob(ext))

        # Process each image
        for image_path in tqdm(image_paths, desc='Processing Images'):
            # Load image in both OpenCV and PIL formats
            img_cv = cv2.imread(str(image_path))
            img_pil = Image.open(image_path)
            draw = ImageDraw.Draw(img_pil)
            
            # Create empty mask for detections
            mask_img = np.zeros(img_cv.shape[:2], dtype=np.uint8)
            
            # Run YOLO detection
            results = model.predict(img_pil)
            detections = []
            
            # Process detection results
            if len(results) > 0 and results[0].boxes.xyxy is not None:
                for box in results[0].boxes:
                    # Extract detection information
                    x1, y1, x2, y2 = box.xyxy[0].tolist()
                    cls_id = int(box.cls.item())
                    conf = box.conf.item()
                    cls_name = results[0].names[cls_id]
                    
                    # Draw bounding box on overlay
                    draw.rectangle([x1, y1, x2, y2], outline=(255, 0, 0), width=3)
                    
                    # Add detection to binary mask
                    cv2.rectangle(mask_img, (int(x1), int(y1)), (int(x2), int(y2)), 255, -1)
                    
                    # Draw label with confidence score
                    label = f"{cls_name}: {conf:.2f}"
                    text_width, text_height = estimate_text_size(label, args['font_size'])
                    draw.rectangle([x1, y1 - text_height - 5, x1 + text_width, y1], fill=(255, 0, 0))
                    draw.text((x1, y1 - text_height - 5), label, fill='white', font=font)
                    
                    # Store detection data for text output
                    detections.append(f"{cls_name} {conf:.2f} {x1} {y1} {x2} {y2}")

            # Save all outputs
            img_pil.save(overlay_dir / image_path.name)  # Annotated image
            cv2.imwrite(str(mask_dir / f"{image_path.stem}.png"), mask_img)  # Binary mask
            with open(detection_dir / f"{image_path.stem}.txt", 'w') as f:  # Detection data
                f.write("\n".join(detections))

        popup.show_message("Generation Complete", f"Processed {len(image_paths)} images.")
        return True

    except Exception as e:
        popup.show_alert("Generation Failed", str(e))
        return False

def estimate_text_size(label: str, font_size: int) -> tuple:
    """
    Estimate the pixel dimensions of text for label placement.

    Args:
        label: The text string to measure
        font_size: Font size in pixels

    Returns:
        tuple: Estimated (width, height) in pixels
    """
    approx_char_width = font_size * 0.6  # Approximate character width
    return (len(label) * approx_char_width, font_size)

def run() -> bool:
    """
    Main entry point providing GUI configuration for detection generation.
    
    Returns:
        bool: True if generation was successful, False otherwise
    """
    # Create configuration form
    form = FormGenerator(title="YOLOv8 Generation Configuration", window_width=700)

    # Configure input fields with validation
    inputs = [
        Input("model_path").path("file"),  # YOLOv8 model file
        Input("input_dir").path("dir"),    # Input images directory
        Input("output_dir").path("dir"),   # Output directory for results
        Input("font_size").type(int).range(10, 100).default(30),  # Label font size
    ]

    for inp in inputs:
        form.add_input(inp)

    # Run generation if form is submitted
    if results := form.show():
        return run_generation(results)
    
    return False
