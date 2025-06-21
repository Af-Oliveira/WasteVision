#!/usr/bin/env python3
"""
train.py - Professional YOLOv8 Training Script

This module provides a GUI-based interface for training YOLOv8 models with features:
- Automatic GPU/CUDA detection and configuration
- Dynamic output directory management
- Comprehensive logging with both file and console output
- Form-based parameter configuration
- Progress tracking and error handling
- Support for various model architectures (nano to extra-large)

The script can be run directly through the GUI or imported for programmatic use:
```python
from scripts.models.yolov8.train import train

results = train({
    'data': 'data.yaml',
    'epochs': 100,
    'batch': 16,
    'device': '0',
    'project': 'runs/train'
})
```
"""

import argparse
import os
from pathlib import Path
import logging
from scripts.utils.utils import get_unique_dir
from scripts.utils.ui.form import FormGenerator
from scripts.utils.ui.popup import PopupManager
from scripts.utils.ui.input import Input
from scripts.models.yolov8.utils.logger import setup_logging
from typing import Optional, Dict, Any, List, Union

import torch
from ultralytics import YOLO


def train(args: Union[Dict[str, Any], argparse.Namespace]) -> Optional[Dict[str, Any]]:
    """
    Execute YOLOv8 training with the given configuration.
    
    Args:
        args: Training configuration containing:
            - data: Path to dataset configuration file (YAML)
            - model: Path to model file or model type (e.g., yolov8n.pt)
            - epochs: Number of training epochs
            - batch: Batch size for training
            - imgsz: Input image size
            - device: Training device (0=CPU, 1=GPU)
            - project: Output directory for results
            - patience: Early stopping patience
            - workers: Number of worker threads
            - logdir: Directory for log files
        
    Returns:
        Dict containing training metrics and paths if successful, None on failure
        
    Raises:
        Various exceptions from YOLO.train() depending on the error condition
    """
    if isinstance(args, argparse.Namespace):
        args = vars(args)
    
    try:
        # Initialize logging with timestamp and directory structure
        setup_logging(args['logdir'])
        logging.info("Starting training with parameters:")
        for k, v in args.items():
            logging.info(f"{k}: {v}")

        # Initialize model and start training
        model = YOLO(args['model'])
        results = model.train(
            data=args['data'],
            epochs=args['epochs'],
            batch=args['batch'],
            imgsz=args['imgsz'],
            device=args['device'],
            project=args['project'],
            patience=args['patience'],
            workers=args['workers']
        )

        logging.info(f"Training completed successfully! Results: {results}")
        return results
        
    except Exception as e:
        logging.error(f"Training failed: {str(e)}")
        raise

def run() -> bool:
    """
    Main entry point providing GUI-based training configuration.
    
    Features:
    - Automatic device detection (CPU/GPU)
    - Form-based parameter input
    - Input validation
    - Progress tracking
    - Error handling with user feedback
    
    Returns:
        bool: True if training completed successfully, False otherwise
    """
    popup_manager = PopupManager()
    
    # Set up output directories
    venv_train_base = Path(os.environ.get('VENV_PATH'), "runs")
    target_dir_runs = get_unique_dir(venv_train_base, "train")
    target_dir_logs = target_dir_runs / "logs"

    # Detect and configure available compute devices
    available_devices = ["0"]  # CPU is always available
    print("CUDA available:", torch.cuda.is_available())
    print("torch version:", torch.__version__)
    print("CUDA version:", torch.version.cuda)
    print("Device count:", torch.cuda.device_count())
    if torch.cuda.is_available():
        available_devices.append("1")  # Add GPU if available

    default_device = "1" if torch.cuda.is_available() else "0"
    print("Available devices:", available_devices)

    # Configure form inputs with validation and defaults
    data_input = Input("data").path('file')  # Dataset configuration
    model_input = Input("model").path('file').default("yolov8n.pt")  # Model architecture
    epochs_input = Input("epochs").type(int).range(1, 1000).default(100)  # Training duration
    batch_input = Input("batch").type(int).range(1, 128).default(16)  # Batch size
    imgsz_input = Input("imgsz").type(int).range(64, 2048).default(640)  # Input resolution
    patience_input = Input("patience").type(int).range(1, 100).default(50)  # Early stopping
    workers_input = Input("workers").type(int).range(1, 32).default(8)  # Data loading threads
    project_input = Input("project").path('dir').default(str(target_dir_runs))  # Output location
    logdir_input = Input("logdir").path('dir').default(str(target_dir_logs))  # Log directory
    device_input = Input("device").options(available_devices).default(default_device)  # Compute device

    # Create and display configuration form
    form = FormGenerator(title="YOLOv8 Training Configuration", window_width=700, window_height=850)
    form.add_input(data_input)
    form.add_input(model_input)
    form.add_input(epochs_input)
    form.add_input(batch_input)
    form.add_input(imgsz_input)
    form.add_input(patience_input)
    form.add_input(workers_input)
    form.add_input(device_input)
    form.add_input(project_input)
    form.add_input(logdir_input)
    
    # Handle form submission or cancellation
    form_results = form.show()
    if not form_results:
        popup_manager.show_message(
            title="Training Cancelled",
            message="Training was cancelled by user",
            consoleprompt=True
        )
        return False
      
    try:
        # Create output directory and start training
        target_dir_runs.mkdir(parents=True, exist_ok=True)
        results = train(form_results)
        
        # Show completion message and log results
        popup_manager.show_message(
            title="Training Complete",
            message=f"Training completed successfully!\nResults saved in: {form_results['project']}",
            width=500,
            height=160,
            consoleprompt=True)
        
        logging.info(f"Training completed successfully! Results saved in: {form_results['project']}")
        return True
        
    except Exception as e:
        # Handle and report training failures
        popup_manager.show_alert(
            title="Training Failed",
            message=f"Training failed: {str(e)}",
            consoleprompt=True
        )
        logging.error(f"Training failed: {str(e)}")
        return False
