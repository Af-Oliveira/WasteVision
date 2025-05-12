from typing import List, Optional, Any, Dict, Union
from scripts.utils.console.option import Option
from scripts.utils.console.action import Action, FunctionAction
import sys
import os


class Menu:
    def __init__(
        self,
        title: str,
        options: Optional[List[Option]] = None,
        parent: Optional['Menu'] = None,
        header: Optional[str] = None,
        footer: Optional[str] = None
    ):
        """
        A interactive menu system with support for submenus and navigation.
        
        Args:
            title: The menu title to display
            options: Initial list of options
            parent: Reference to parent menu (for back navigation)
            header: Additional text to display at the top of the menu
            footer: Additional text to display at the bottom of the menu
        """
        self.title = title
        self.options = options or []
        self.parent = parent
        self.header = header
        self.footer = footer
        self._init_default_options()
    
    def _init_default_options(self) -> None:
        """Initialize the default navigation options."""
        if self.parent:
            self.add_option(Option(
                name="back",
                description="Return to previous menu",
                action=FunctionAction(lambda: None)  # Back is handled in display()
            ))
        
        self.exit_option = Option(
            name="0",
            description="Exit program",
            action=FunctionAction(lambda: None)  # Exit is handled in display()
        )
    
    def add_option(self, option: Option) -> None:
        """Add a single option to the menu."""
        self.options.append(option)
    
    def add_options(self, options: List[Option]) -> None:
        """Add multiple options to the menu."""
        self.options.extend(options)
    
    def create_submenu(
        self,
        title: str,
        options: List[Option],
        header: Optional[str] = None,
        footer: Optional[str] = None
    ) -> 'Menu':
        """Create and return a new submenu with this menu as parent."""
        return Menu(title, options, parent=self, header=header, footer=footer)
    
    def display(self) -> Optional[Any]:
        """
        Display the menu and handle user interaction.
        
        Returns:
            The result of the executed option, or None if exited/back
        """
        while True:
            self._clear_screen()
            self._print_header()
            
            # Display visible options
            visible_options = [opt for opt in self.options if opt.visible]
            for i, option in enumerate(visible_options, start=1):
                print(f"{i}. {option}")
            
            self._print_footer()
            
            # Get user choice
            choice = input("\nEnter your choice: ").strip().lower()
            
            # Handle special options
            if choice == "0":
                print("\nExiting program...")
                return None
            elif choice == "back" and self.parent:
                print("\nReturning to previous menu...")
                return None
            
            # Validate and execute
            try:
                choice_idx = int(choice) - 1
                if 0 <= choice_idx < len(visible_options):
                    selected_option = visible_options[choice_idx]
                    
                    if not selected_option.enabled:
                        print("\nThis option is currently disabled.")
                        input("Press Enter to continue...")
                        continue
                    
                    print(f"\nExecuting: {selected_option.description}...")
                    result = selected_option.execute()
                    
                    # If the action returns a Menu, display it
                    if isinstance(result, Menu):
                        result.display()
                    elif result is not None:
                        # Return non-Menu results to caller
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
        """Print the menu header section."""
        print(f"\n{self.title}")
        print("=" * len(self.title))
        if self.header:
            print(f"\n{self.header}")
    
    def _print_footer(self) -> None:
        """Print the menu footer section."""
        if self.footer:
            print(f"\n{self.footer}")
        print(f"\n{self.exit_option.name}. {self.exit_option.description}")
        if self.parent:
            print("back. Return to previous menu")
    
    def _clear_screen(self) -> None:
        """Clear the console screen in a cross-platform way."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def run_as_main(self) -> None:
        """Run the menu as the main program interface."""
        while True:
            result = self.display()
            if result is None:  # User chose to exit
                break
            # Optional: handle returned results from options