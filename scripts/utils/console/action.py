import importlib
import sys
from typing import Any, Optional, Callable, Dict, List


class Action:
    def __init__(
        self,
        script_path: str,
        entry_function: str = "run",
        args: Optional[List[Any]] = None,
        kwargs: Optional[Dict[str, Any]] = None
    ):
        """
        Represents an executable action that can be performed by a menu option.
        
        Args:
            script_path: Path to the Python script/module (e.g., "scripts.process_data")
            entry_function: Name of the function to call (default "run")
            args: Positional arguments for the entry function
            kwargs: Keyword arguments for the entry function
        """
        self.script_path = script_path
        self.entry_function = entry_function
        self.args = args or []
        self.kwargs = kwargs or {}
    
    def execute(self) -> Any:
        """
        Execute the associated script's entry function with provided arguments.
        
        Returns:
            The return value of the called function.
            
        Raises:
            ImportError: If the module cannot be imported
            AttributeError: If the function doesn't exist in the module
            Exception: Any exception raised by the called function
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
        """String representation for debugging."""
        args_str = ', '.join(map(str, self.args))
        kwargs_str = ', '.join(f"{k}={v}" for k, v in self.kwargs.items())
        all_args = ', '.join(filter(None, [args_str, kwargs_str]))
        return f"Action({self.script_path}.{self.entry_function}({all_args}))"


class FunctionAction(Action):
    """Action that executes a direct function call rather than importing a module."""
    
    def __init__(self, func: Callable, args: Optional[List[Any]] = None, kwargs: Optional[Dict[str, Any]] = None):
        """
        Initialize with a direct function reference.
        
        Args:
            func: The function to call
            args: Positional arguments for the function
            kwargs: Keyword arguments for the function
        """
        self.func = func
        self.args = args or []
        self.kwargs = kwargs or {}
    
    def execute(self) -> Any:
        """Execute the function directly."""
        try:
            return self.func(*self.args, **self.kwargs)
        except Exception as e:
            print(f"Error executing function {self.func.__name__}: {str(e)}", file=sys.stderr)
            raise