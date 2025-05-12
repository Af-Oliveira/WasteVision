# Imports
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
    """Execute detection-only generation with GUI parameters."""
    popup = PopupManager()
    try:
        # Setup directories
        input_dir = Path(args['input_dir'])
        output_dir = Path(args['output_dir'])
        overlay_dir = output_dir / 'overlays'
        detection_dir = output_dir / 'detections'
        mask_dir = output_dir / 'masks'

        # Create directories
        for dir in [overlay_dir, detection_dir, mask_dir]:
            dir.mkdir(parents=True, exist_ok=True)

        # Load model
        model = YOLO(args['model_path'])

        # Font setup
        try:
            font = ImageFont.load_default(size=args['font_size'])
        except:
            font = ImageFont.load_default()

        # Process images
        image_paths = []
        for ext in ['*.jpg', '*.jpeg', '*.png']:
            image_paths.extend(input_dir.glob(ext))

        # Detection processing loop
        for image_path in tqdm(image_paths, desc='Processing Images'):
            # Load image
            img_cv = cv2.imread(str(image_path))
            img_pil = Image.open(image_path)
            draw = ImageDraw.Draw(img_pil)
            
            # Initialize blank mask
            mask_img = np.zeros(img_cv.shape[:2], dtype=np.uint8)
            
            # Run detection
            results = model.predict(img_pil)
            detections = []
            
            if len(results) > 0 and results[0].boxes.xyxy is not None:
                for box in results[0].boxes:
                    x1, y1, x2, y2 = box.xyxy[0].tolist()
                    cls_id = int(box.cls.item())
                    conf = box.conf.item()
                    cls_name = results[0].names[cls_id]
                    
                    # Draw bounding box (red by default)
                    draw.rectangle([x1, y1, x2, y2], outline=(255, 0, 0), width=3)
                    
                    # Add to mask
                    cv2.rectangle(mask_img, (int(x1), int(y1)), (int(x2), int(y2)), 255, -1)
                    
                    # Draw label if enabled
                    label = f"{cls_name}: {conf:.2f}"
                    text_width, text_height = estimate_text_size(label, args['font_size'])
                    draw.rectangle([x1, y1 - text_height - 5, x1 + text_width, y1], fill=(255, 0, 0))
                    draw.text((x1, y1 - text_height - 5), label, fill='white', font=font)
                    
                    detections.append(f"{cls_name} {conf:.2f} {x1} {y1} {x2} {y2}")

            # Save outputs
            img_pil.save(overlay_dir / image_path.name)
            cv2.imwrite(str(mask_dir / f"{image_path.stem}.png"), mask_img)
            
            # Write detections to file
            with open(detection_dir / f"{image_path.stem}.txt", 'w') as f:
                f.write("\n".join(detections))

        popup.show_message("Generation Complete", f"Processed {len(image_paths)} images.")
        return True

    except Exception as e:
        popup.show_alert("Generation Failed", str(e))
        return False


def estimate_text_size(label: str, font_size: int) -> tuple:
    """Helper to estimate text dimensions."""
    approx_char_width = font_size * 0.6
    return (len(label) * approx_char_width, font_size)

def run() -> bool:
    """GUI entry point."""
    form = FormGenerator(title="YOLOv8 Generation Configuration", window_width=700)

    # Form inputs
    inputs = [
        Input("model_path").path("file"),
        Input("input_dir").path("dir"),
        Input("output_dir").path("dir"),
        Input("font_size").type(int).range(10, 100).default(30),
    ]

    for inp in inputs:
        form.add_input(inp)

    if results := form.show():
        run_generation(results)
