# main.py - Test script for virtualenv auto-run
from scripts.utils.console.option import Option
from scripts.utils.console.menu import Menu
from scripts.utils.console.action import Action


def main():
    try:
        menu = create_main_menu()
        menu.run_as_main()
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"An error occurred: {e}")


def create_main_menu() -> Menu:
    """Create and configure the main menu system."""
    main_menu = Menu(
        title="YOLO Venv Manager",
        header="Welcome to the YOLO Venv Management System",
        footer="Select an option to continue"
    )
    
    # Option 1: Install Requirements
    main_menu.add_option(Option(
        name="Install",
        description="Install YOLO requirements",
        action=Action(
            script_path="scripts.models.yolov8.utils.install_reqs",  # This will run install_reqs.py via command line
        )
    ))

    # Option 2: Run Training (with argument examples)
    main_menu.add_option(Option(
        name="Train",
        description="Run YOLO training ",
        action=Action(
            script_path="scripts.models.yolov8.train",         # This will run train.py via command line
        )
    ))

    
    # Option 2: Run Training (with argument examples)
    main_menu.add_option(Option(
        name="Run",
        description="Detect YOLO", 
        action=Action(
            script_path="scripts.models.yolov8.generate",         # This will run train.py via command line
        )
    ))

     # Option 2: Run Training (with argument examples)
    main_menu.add_option(Option(
        name="Export",
        description="Export model", 
        action=Action(
            script_path="scripts.models.yolov8.utils.exporter",         # This will run train.py via command line
        )
    ))
    

    return main_menu
    

if __name__ == "__main__":
    main()
