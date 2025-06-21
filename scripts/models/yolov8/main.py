"""
main.py - YOLOv8 Management Interface

This module provides a console-based menu interface for managing YOLOv8 operations:
- Installing dependencies and requirements
- Training models with custom datasets
- Running object detection on images/video
- Exporting models to different formats

The menu system uses the custom console UI framework to provide a user-friendly
interface for accessing different YOLOv8 functionalities.
"""

from scripts.utils.console.option import Option
from scripts.utils.console.menu import Menu
from scripts.utils.console.action import Action


def main():
    """
    Entry point for the YOLOv8 management interface.
    
    Handles the creation and execution of the main menu system with
    error handling for graceful exit on interrupts.
    """
    try:
        menu = create_main_menu()
        menu.run_as_main()
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"An error occurred: {e}")


def create_main_menu() -> Menu:
    """
    Create and configure the main menu system for YOLOv8 management.
    
    Returns:
        Menu: Configured menu instance with the following options:
            1. Install - Install YOLOv8 requirements
            2. Train - Run model training
            3. Run - Execute object detection
            4. Export - Export model to different formats
    """
    main_menu = Menu(
        title="YOLO Venv Manager",
        header="Welcome to the YOLO Venv Management System",
        footer="Select an option to continue"
    )
    
    # Install Requirements Option
    main_menu.add_option(Option(
        name="Install",
        description="Install YOLOv8 requirements",
        action=Action(
            script_path="scripts.models.yolov8.utils.install_reqs"
        )
    ))

    # Model Training Option
    main_menu.add_option(Option(
        name="Train",
        description="Run YOLOv8 model training",
        action=Action(
            script_path="scripts.models.yolov8.train"
        )
    ))

    # Object Detection Option
    main_menu.add_option(Option(
        name="Run",
        description="Execute YOLOv8 object detection", 
        action=Action(
            script_path="scripts.models.yolov8.generate"
        )
    ))

    # Model Export Option
    main_menu.add_option(Option(
        name="Export",
        description="Export YOLOv8 model to other formats", 
        action=Action(
            script_path="scripts.models.yolov8.utils.exporter"
        )
    ))

    return main_menu


if __name__ == "__main__":
    main()
