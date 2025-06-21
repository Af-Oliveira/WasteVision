
"""
exporter.py - YOLOv8 Model Export Utility

This module provides functionality to export YOLOv8 models to different formats,
particularly optimized for edge devices like Raspberry Pi. It features:

- GUI-based configuration using custom form inputs
- Support for NCNN format optimization
- Comprehensive error handling and user feedback
- Flexible model size configuration
- Model simplification options for better performance

The script can be run directly or imported as a module for programmatic use.
"""

import argparse
from scripts.utils.ui.form import FormGenerator
from scripts.utils.ui.popup import PopupManager
from scripts.utils.ui.input import Input
from typing import Optional, Dict, Any, Union
from ultralytics import YOLO

# Currently supported export formats
# Note: NCNN is prioritized for Raspberry Pi deployment
SUPPORTED_FORMATS = [
    "ncnn"  # Neural Compute Neural Networks format
]

def export_model(args: Union[Dict[str, Any], argparse.Namespace]) -> Optional[Dict[str, Any]]:
    """
    Export a YOLOv8 model to the specified format with given configuration.
    
    Args:
        args: Export configuration containing:
            - model: Path to the source model file (.pt)
            - format: Target export format (e.g., "ncnn")
            - imgsz: Input image size for the model
            - simplify: Whether to optimize model structure
        
    Returns:
        Dict containing export results and paths if successful, None otherwise
        
    Raises:
        Various exceptions from YOLO.export() depending on the error condition
    """
    if isinstance(args, argparse.Namespace):
        args = vars(args)
    
    try:
        # Initialize model and perform export
        model = YOLO(args['model'])
        results = model.export(
            format=args['format'],
            imgsz=args['imgsz'],
            simplify=args['simplify']
        )
        return results
        
    except Exception as e:
        # Re-raise the exception for handling by the caller
        raise

def run() -> bool:
    """
    Main entry point providing a GUI interface for model export configuration.
    
    Features:
    - Form-based input for export parameters
    - Input validation and constraints
    - Visual feedback for export status
    - Error handling with user-friendly messages
    
    Returns:
        bool: True if export completed successfully, False otherwise
    """
    popup_manager = PopupManager()

    # Configure form inputs with validation and defaults
    model_input = Input("model").path('file').default("yolov8n.pt")
    format_input = Input("format").options(SUPPORTED_FORMATS).default("ncnn")
    imgsz_input = Input("imgsz").type(int).range(64, 2048).default(640)
    simplify_input = Input("simplify").type(bool).default(True)

    # Create and display the configuration form
    form = FormGenerator(
        title="YOLOv8 Model Export Configuration",
        window_width=700,
        window_height=700
    )
    form.add_input(model_input)
    form.add_input(format_input)
    form.add_input(imgsz_input)
    form.add_input(simplify_input)
    
    # Get user input
    form_results = form.show()
    
    # Handle form cancellation
    if not form_results:
        popup_manager.show_message(
            title="Export Cancelled",
            message="Model export was cancelled by user",
            consoleprompt=True
        )
        return False
      
    try:
        # Perform model export with selected configuration
        results = export_model(form_results)
        popup_manager.show_message(
            title="Export Complete",
            message=f"Model exported successfully!\nResults saved.",
            width=500,
            height=160,
            consoleprompt=True
        )
        return True
        
    except Exception as e:
        # Handle export failures with user feedback
        popup_manager.show_alert(
            title="Export Failed",
            message=f"Model export failed: {str(e)}",
            consoleprompt=True
        )
        return False

if __name__ == "__main__":
    run()