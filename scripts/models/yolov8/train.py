#!/usr/bin/env python3
"""
Professional YOLOv8 Training Script

Features:
- GPU/CUDA auto-detection
- Custom output directories
- Comprehensive logging
- Argument-driven training control

Usage:
    python train.py --data data.yaml --epochs 100 --batch 16 --device 0 --project runs/train --name exp1
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
    Execute YOLOv8 training with given configuration.
    
    Args:
        args: Training configuration (dict or Namespace)
        
    Returns:
        Training results if successful, None otherwise
    """
    if isinstance(args, argparse.Namespace):
        args = vars(args)
    
    try:
        # Initialize logging
        setup_logging(args['logdir'])
        logging.info("Starting training with parameters:")
        for k, v in args.items():
            logging.info(f"{k}: {v}")

        # Model setup and training
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
    Main entry point for the script with GUI form support.
    """
    popup_manager = PopupManager()
    venv_train_base = Path(os.environ.get('VENV_PATH'), "runs")
    target_dir_runs = get_unique_dir(venv_train_base, "train")
    target_dir_logs = target_dir_runs / "logs"

    # Detect available devices
    available_devices = ["0"]  # 0 always represents CPU
    print("CUDA available:", torch.cuda.is_available())
    print("torch version:", torch.__version__)
    print("CUDA version:", torch.version.cuda)
    print("Device count:", torch.cuda.device_count())
    if torch.cuda.is_available():
        available_devices.append("1")  # 1 represents GPU

    default_device = "1" if torch.cuda.is_available() else "0"
    print ("Available devices:", available_devices)
    # Create form inputs
    data_input = Input("data").path('file')
    model_input = Input("model").path('file').default("yolov8n.pt")
    epochs_input = Input("epochs").type(int).range(1, 1000).default(100)
    batch_input = Input("batch").type(int).range(1, 128).default(16)
    imgsz_input = Input("imgsz").type(int).range(64, 2048).default(640)
    patience_input = Input("patience").type(int).range(1, 100).default(50)
    workers_input = Input("workers").type(int).range(1, 32).default(8)
    project_input = Input("project").path('dir').default(str(target_dir_runs))
    logdir_input = Input("logdir").path('dir').default(str(target_dir_logs))
    device_input = Input("device").options(available_devices).default(default_device)

    # Create and show form
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
    
    form_results = form.show()
    
    if not form_results:
        popup_manager.show_message(
            title="Training Cancelled",
            message="Training was cancelled by user",
            consoleprompt=True
        )
        return False
      
    try:
        # Train the model
        target_dir_runs.mkdir(parents=True, exist_ok=True)
        results = train(form_results)
        popup_manager.show_message(
            title="Training Complete",
            message=f"Training completed successfully!\nResults saved in: {form_results['project']}",
            width=500,
            height=160,
            consoleprompt=True)
        
        logging.info(f"Training completed successfully! Results saved in: {form_results['project']}")
        return True
    except Exception as e:
        popup_manager.show_alert(
            title="Training Failed",
            message=f"Training failed: {str(e)}",
            consoleprompt=True
        )
        logging.error(f"Training failed: {str(e)}")
        return False
