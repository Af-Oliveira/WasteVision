"""
action.py - Action execution system for WasteVision console menus

This module provides two classes for handling menu actions:
- Action: Executes functions from imported modules
- FunctionAction: Executes direct function references

These classes are used throughout the project to create interactive menus
and handle user commands in a consistent way. They support argument passing,
error handling, and detailed execution feedback.
"""

import importlib
import sys
from typing import Any, Optional, Callable, Dict, List


class Action:
    """
    Represents an executable action that can be performed by a menu option.
    
    This class handles dynamic module imports and function execution, with
    comprehensive error handling and debugging support. It is primarily used
    to create menu options that execute specific Python modules/scripts.
    """

    def __init__(
        self,
        script_path: str,
        entry_function: str = "run",
        args: Optional[List[Any]] = None,
        kwargs: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize an action with a script path and execution parameters.
        
        Args:
            script_path: Dot-notation path to the Python module (e.g., "scripts.process_data")
            entry_function: Name of the function to call within the module (defaults to "run")
            args: List of positional arguments to pass to the entry function
            kwargs: Dictionary of keyword arguments to pass to the entry function
        """
        self.script_path = script_path
        self.entry_function = entry_function
        self.args = args or []
        self.kwargs = kwargs or {}
    
    def execute(self) -> Any:
        """
        Execute the associated script's entry function with provided arguments.
        
        The method will:
        1. Import the specified module
        2. Verify the entry function exists
        3. Execute the function with provided arguments
        4. Handle and report any errors that occur
        
        Returns:
            Any: The return value from the executed function
            
        Raises:
            ImportError: If the specified module cannot be imported
            AttributeError: If the entry function doesn't exist in the module
            Exception: Any exception raised during function execution
        """
        try:
            module = importlib.import_module(self.script_path)
            
            if not hasattr(module, self.entry_function):
                available = [attr for attr in dir(module) if not attr.startswith('_')]
                raise AttributeError(
                    f"Module '{self.script_path}' has no '{self.entry_function}' function. "
                    f"Available functions: {', '.join(available)}"
                )
            
            func = getattr(module, self.entry_function)
            result = func(*self.args, **self.kwargs)
            return result
            
        except ImportError as e:
            print(f"Error importing '{self.script_path}': {str(e)}", file=sys.stderr)
            raise
        except AttributeError as e:
            print(str(e), file=sys.stderr)
            raise
        except Exception as e:
            print(f"Error executing {self.script_path}.{self.entry_function}(): {str(e)}", file=sys.stderr)
            raise

    def __str__(self) -> str:
        """
        Create a string representation of the Action for debugging.
        
        Returns:
            str: A formatted string showing the action's configuration
                 (e.g., "Action(scripts.process_data.run(arg1, kwarg1=value1))")
        """
        args_str = ', '.join(map(str, self.args))
        kwargs_str = ', '.join(f"{k}={v}" for k, v in self.kwargs.items())
        all_args = ', '.join(filter(None, [args_str, kwargs_str]))
        return f"Action({self.script_path}.{self.entry_function}({all_args}))"


class FunctionAction(Action):
    """
    Specialized Action that executes a direct function reference.
    
    This class provides a simpler alternative to Action when you already
    have a reference to the function you want to execute, rather than
    importing it from a module.
    """
    
    def __init__(self, func: Callable, args: Optional[List[Any]] = None, kwargs: Optional[Dict[str, Any]] = None):
        """
        Initialize with a direct function reference and its arguments.
        
        Args:
            func: The function to execute when the action is triggered
            args: List of positional arguments to pass to the function
            kwargs: Dictionary of keyword arguments to pass to the function
        """
        self.func = func
        self.args = args or []
        self.kwargs = kwargs or {}
    
    def execute(self) -> Any:
        """
        Execute the stored function with its arguments.
        
        Returns:
            Any: The return value from the executed function
            
        Raises:
            Exception: Any exception raised during function execution
        """
        try:
            return self.func(*self.args, **self.kwargs)
        except Exception as e:
            print(f"Error executing function {self.func.__name__}: {str(e)}", file=sys.stderr)
            raise