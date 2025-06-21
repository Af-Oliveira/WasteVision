"""
menu.py - Interactive Console Menu System for WasteVision

This module provides a flexible and robust console menu system that supports:
- Hierarchical menu structures with parent/child relationships
- Dynamic option visibility and enablement
- Custom headers and footers
- Cross-platform operation
- Action execution and result handling
- Navigation between menus
"""

from typing import List, Optional, Any, Dict, Union
from scripts.utils.console.option import Option
from scripts.utils.console.action import Action, FunctionAction
import sys
import os


class Menu:
    """
    An interactive console menu system with hierarchical navigation.
    
    This class implements a full-featured console menu system that supports:
    - Multiple levels of nested submenus
    - Dynamic option management (add/remove/modify)
    - Conditional option visibility and enablement
    - Customizable display with headers and footers
    - Error handling and user input validation
    - Cross-platform screen clearing
    
    The menu system is designed to be both user-friendly and developer-friendly,
    with clear error messages and a consistent navigation model.
    """

    def __init__(
        self,
        title: str,
        options: Optional[List[Option]] = None,
        parent: Optional['Menu'] = None,
        header: Optional[str] = None,
        footer: Optional[str] = None
    ):
        """
        Initialize a new menu with the specified configuration.
        
        Args:
            title: The menu title displayed at the top
            options: List of menu options (Option objects)
            parent: Parent menu for hierarchical navigation
            header: Text to display below the title
            footer: Text to display above the navigation options
        """
        self.title = title
        self.options = options or []
        self.parent = parent
        self.header = header
        self.footer = footer
        self._init_default_options()
    
    def _init_default_options(self) -> None:
        """
        Initialize the standard navigation options (back/exit).
        
        Adds:
        - "back" option if this is a submenu
        - "exit" option for all menus
        """
        if self.parent:
            self.add_option(Option(
                name="back",
                description="Return to previous menu",
                action=FunctionAction(lambda: None)  # Handled in display()
            ))
        
        self.exit_option = Option(
            name="0",
            description="Exit program",
            action=FunctionAction(lambda: None)  # Handled in display()
        )
    
    def add_option(self, option: Option) -> None:
        """
        Add a single option to the menu.
        
        Args:
            option: The Option object to add
        """
        self.options.append(option)
    
    def add_options(self, options: List[Option]) -> None:
        """
        Add multiple options to the menu at once.
        
        Args:
            options: List of Option objects to add
        """
        self.options.extend(options)
    
    def create_submenu(
        self,
        title: str,
        options: List[Option],
        header: Optional[str] = None,
        footer: Optional[str] = None
    ) -> 'Menu':
        """
        Create a new submenu connected to this menu.
        
        Args:
            title: Title for the submenu
            options: List of options for the submenu
            header: Optional header text
            footer: Optional footer text
            
        Returns:
            Menu: A new Menu instance with this menu as its parent
        """
        return Menu(title, options, parent=self, header=header, footer=footer)
    
    def display(self) -> Optional[Any]:
        """
        Display the menu and process user input.
        
        This method:
        1. Clears the screen
        2. Shows the menu title and header
        3. Lists all visible options
        4. Shows the footer and navigation options
        5. Processes user input and executes selected options
        
        Returns:
            Optional[Any]: The result from executing an option, or None for exit/back
        """
        while True:
            self._clear_screen()
            self._print_header()
            
            # Show only visible options
            visible_options = [opt for opt in self.options if opt.visible]
            for i, option in enumerate(visible_options, start=1):
                print(f"{i}. {option}")
            
            self._print_footer()
            
            # Handle user input
            choice = input("\nEnter your choice: ").strip().lower()
            
            # Process navigation commands
            if choice == "0":
                print("\nExiting program...")
                return None
            elif choice == "back" and self.parent:
                print("\nReturning to previous menu...")
                return None
            
            # Execute selected option
            try:
                choice_idx = int(choice) - 1
                if 0 <= choice_idx < len(visible_options):
                    selected_option = visible_options[choice_idx]
                    
                    # Check if option is enabled
                    if not selected_option.enabled:
                        print("\nThis option is currently disabled.")
                        input("Press Enter to continue...")
                        continue
                    
                    # Execute the option's action
                    print(f"\nExecuting: {selected_option.description}...")
                    result = selected_option.execute()
                    
                    # Handle special case where option returns a submenu
                    if isinstance(result, Menu):
                        result.display()
                    elif result is not None:
                        return result
                    
                    input("\nPress Enter to continue...")
                else:
                    print("\nInvalid choice. Please enter a valid number.")
                    input("Press Enter to continue...")
            except ValueError:
                print("\nPlease enter a number corresponding to your choice.")
                input("Press Enter to continue...")
            except Exception as e:
                print(f"\nError executing option: {str(e)}", file=sys.stderr)
                input("Press Enter to continue...")
    
    def _print_header(self) -> None:
        """
        Display the menu header section.
        
        Shows:
        1. Menu title with underline
        2. Optional header text
        """
        print(f"\n{self.title}")
        print("=" * len(self.title))
        if self.header:
            print(f"\n{self.header}")
    
    def _print_footer(self) -> None:
        """
        Display the menu footer section.
        
        Shows:
        1. Optional footer text
        2. Exit option
        3. Back option (if this is a submenu)
        """
        if self.footer:
            print(f"\n{self.footer}")
        print(f"\n{self.exit_option.name}. {self.exit_option.description}")
        if self.parent:
            print("back. Return to previous menu")
    
    def _clear_screen(self) -> None:
        """
        Clear the terminal screen in a cross-platform way.
        
        Uses 'cls' for Windows and 'clear' for Unix-like systems.
        """
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def run_as_main(self) -> None:
        """
        Run this menu as the main program interface.
        
        Continuously displays the menu until the user chooses to exit.
        """
        while True:
            result = self.display()
            if result is None:  # User chose to exit
                break