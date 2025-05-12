#!/usr/bin/env python3
"""
Professional YOLOv8 Export Script

Features:
- Model format selection
- Custom output directories
- Comprehensive logging
- Argument-driven export control

Usage:
    python exporter.py --model path/to/model.pt --format ncnn --imgsz 640
"""

import argparse
from scripts.utils.ui.form import FormGenerator
from scripts.utils.ui.popup import PopupManager
from scripts.utils.ui.input import Input
from typing import Optional, Dict, Any, Union

from ultralytics import YOLO

# Supported export formats
SUPPORTED_FORMATS = [
"ncnn"
]

def export_model(args: Union[Dict[str, Any], argparse.Namespace]) -> Optional[Dict[str, Any]]:
    """
    Execute YOLOv8 model export with given configuration.
    
    Args:
        args: Export configuration (dict or Namespace)
        
    Returns:
        Export results if successful, None otherwise
    """
    if isinstance(args, argparse.Namespace):
        args = vars(args)
    
    try:

        # Model setup and export
        model = YOLO(args['model'])
        results = model.export(
            format=args['format'],
            imgsz=args['imgsz'],
            optimize=args['optimize'],
            simplify=args['simplify']
        )

       
        return results
        
    except Exception as e:
       
        raise

def run() -> bool:
    """
    Main entry point for the script with GUI form support.
    """
    popup_manager = PopupManager()

    # Create form inputs
    model_input = Input("model").path('file').default("yolov8n.pt")
    format_input = Input("format").options(SUPPORTED_FORMATS).default("ncnn")
    imgsz_input = Input("imgsz").type(int).range(64, 2048).default(640)
    optimize_input = Input("optimize").type(bool).default(True)
    simplify_input = Input("simplify").type(bool).default(True)

    # Create and show form
    form = FormGenerator(title="YOLOv8 Model Export Configuration", window_width=700, window_height=700)
    form.add_input(model_input)
    form.add_input(format_input)
    form.add_input(imgsz_input)
    form.add_input(optimize_input)
    form.add_input(simplify_input)
    
    form_results = form.show()
    
    if not form_results:
        popup_manager.show_message(
            title="Export Cancelled",
            message="Model export was cancelled by user",
            consoleprompt=True
        )
        return False
      
    try:
        # Export the model
        results = export_model(form_results)
        popup_manager.show_message(
            title="Export Complete",
            message=f"Model exported successfully!\nResults saved.",
            width=500,
            height=160,
            consoleprompt=True)
        
       
        return True
    except Exception as e:
        popup_manager.show_alert(
            title="Export Failed",
            message=f"Model export failed: {str(e)}",
            consoleprompt=True
        )
        
        return False

if __name__ == "__main__":
    run()