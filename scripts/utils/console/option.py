from typing import Any, Optional, List, Dict, Union
from dataclasses import dataclass
from scripts.utils.console.action import Action


@dataclass
class Option:
    """
    Represents a selectable menu option with an associated action.
    
    Attributes:
        name: Short identifier for the option (e.g., "1" or "back")
        description: Help text describing the option
        action: The Action to execute when this option is selected
        enabled: Whether this option is currently selectable
        visible: Whether this option should be displayed
    """
    name: str
    description: str
    action: Action
    enabled: bool = True
    visible: bool = True
    
    def execute(self) -> Any:
        """
        Execute the associated action if enabled.
        
        Returns:
            The result of the action execution.
            
        Raises:
            RuntimeError: If the option is disabled
            Exception: Any exception raised by the action
        """
        if not self.enabled:
            raise RuntimeError(f"Cannot execute disabled option: {self.name}")
        
        return self.action.execute()
    
    def set_enabled(self, enabled: bool) -> None:
        """Set whether this option is enabled."""
        self.enabled = enabled
    
    def set_visible(self, visible: bool) -> None:
        """Set whether this option is visible."""
        self.visible = visible
    
    def __str__(self) -> str:
        """User-friendly string representation."""
        status = "" if self.enabled else " (disabled)"
        return f"{self.name}: {self.description}{status}"