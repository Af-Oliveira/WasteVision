import logging
from datetime import datetime
from pathlib import Path
from typing import Union


def setup_logging(log_dir: Union[str, Path]) -> str:
    """
    Configure logging for YOLOv8 training with both file and console output.
    
    Args:
        log_dir: Directory where log files will be stored        
    Returns:
        Path to the log file
    """
    log_dir = Path(log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Create unique log file name with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_dir / f"log_{timestamp}.log"
    
    # Clear any existing handlers
    logging.getLogger().handlers.clear()
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file),  # File handler
            logging.StreamHandler()        # Console handler
        ]
    )
    
    # Configure Ultralytics/YOLO logging
    yolo_logger = logging.getLogger("ultralytics")
    yolo_logger.setLevel(logging.INFO)
    yolo_logger.propagate = False
    
    # Add YOLO metrics to our log file
    metrics_handler = logging.FileHandler(log_file)
    metrics_handler.setLevel(logging.INFO)
    yolo_logger.addHandler(metrics_handler)
    
    logging.info(f"Logging initialized. Log file: {log_file}")
    return str(log_file)