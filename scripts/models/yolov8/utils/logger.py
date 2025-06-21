"""
logger.py - YOLOv8 Training Logger Configuration

This module provides logging setup for YOLOv8 model training, with features:
- Timestamped log files for each training session
- Dual output to both file and console
- Custom formatting for clear message presentation
- Integration with Ultralytics YOLO logging system 
- Metrics tracking and storage
- Automatic log directory creation
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Union


def setup_logging(log_dir: Union[str, Path]) -> str:
    """
    Configure logging for YOLOv8 training with both file and console output.
    
    This function sets up a comprehensive logging system that:
    - Creates timestamped log files
    - Outputs to both file and console
    - Integrates with YOLO's internal logging
    - Tracks training metrics
    
    Args:
        log_dir: Directory where log files will be stored. Created if doesn't exist.
        
    Returns:
        str: Absolute path to the created log file.
        
    Example:
        ```python
        log_file = setup_logging("training_logs")
        # Log file will be like: training_logs/log_20250519_143022.log
        ```
    """
    # Convert to Path object and ensure directory exists
    log_dir = Path(log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Create unique log file name with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_dir / f"log_{timestamp}.log"
    
    # Clear any existing handlers to avoid duplicate logging
    logging.getLogger().handlers.clear()
    
    # Configure root logger with both file and console output
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file),  # Log to file
            logging.StreamHandler()         # Log to console
        ]
    )
    
    # Configure Ultralytics/YOLO specific logging
    yolo_logger = logging.getLogger("ultralytics")
    yolo_logger.setLevel(logging.INFO)
    yolo_logger.propagate = False  # Prevent duplicate messages
    
    # Ensure YOLO metrics are captured in our log file
    metrics_handler = logging.FileHandler(log_file)
    metrics_handler.setLevel(logging.INFO)
    yolo_logger.addHandler(metrics_handler)
    
    # Log initialization success
    logging.info(f"Logging initialized. Log file: {log_file}")
    return str(log_file)