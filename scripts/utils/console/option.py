"""
option.py - Menu option handling for WasteVision console menus

This module provides the Option class which represents selectable menu items
that can execute actions when chosen. It supports:
- Dynamic enabling/disabling of options
- Visibility control for conditional display
- Action execution with error handling
- User-friendly string representations
- Integration with the Action system
"""

from typing import Any, Optional, List, Dict, Union
from dataclasses import dataclass
from scripts.utils.console.action import Action


@dataclass
class Option:
    """
    Represents a selectable menu option with an associated action.
    
    This class handles individual menu options, managing their state and execution.
    It works in conjunction with the Menu and Action classes to provide a complete
    menu system.
    
    Attributes:
        name (str): Short identifier for the option (e.g., "1", "back", "train")
        description (str): User-friendly description of what the option does
        action (Action): The Action object to execute when this option is selected
        enabled (bool): Whether this option can currently be selected (default: True)
        visible (bool): Whether this option should be shown in the menu (default: True)
    
    Example:
        ```python
        option = Option(
            name="1",
            description="Train new model",
            action=Action("scripts.models.train", "run"),
            enabled=True,
            visible=True
        )
        ```
    """
    name: str
    description: str
    action: Action
    enabled: bool = True
    visible: bool = True
    
    def execute(self) -> Any:
        """
        Execute the option's associated action if the option is enabled.
        
        This method first checks if the option is enabled, then delegates to
        the action's execute() method if it is.
        
        Returns:
            Any: The result returned by the action's execution
            
        Raises:
            RuntimeError: If attempting to execute a disabled option
            Exception: Any exception raised during action execution
        """
        if not self.enabled:
            raise RuntimeError(f"Cannot execute disabled option: {self.name}")
        
        return self.action.execute()
    
    def set_enabled(self, enabled: bool) -> None:
        """
        Set whether this option can be selected.
        
        Args:
            enabled (bool): True to enable the option, False to disable it
        """
        self.enabled = enabled
    
    def set_visible(self, visible: bool) -> None:
        """
        Set whether this option should be displayed in the menu.
        
        Args:
            visible (bool): True to show the option, False to hide it
        """
        self.visible = visible
    
    def __str__(self) -> str:
        """
        Create a user-friendly string representation of the option.
        
        The string includes the option's name, description, and disabled status
        if applicable.
        
        Returns:
            str: Formatted string like "1: Train new model" or "2: Export model (disabled)"
        """
        status = "" if self.enabled else " (disabled)"
        return f"{self.name}: {self.description}{status}"