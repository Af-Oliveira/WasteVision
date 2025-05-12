
import re
from typing import Any, Callable, Optional, Union, Type, List, Tuple
from pathlib import Path


class Input:
    """
    A robust console input handler with validation and type checking.
    
    Features:
    - Type validation (int, float, str, bool, etc.)
    - Custom validation functions
    - Range checking for numbers
    - Pattern matching for strings
    - Automatic retry on invalid input
    - Custom error messages
    - Default values
    - Menu integration support
    - Multiple option selection
    """

    def __init__(self, prompt: str = ""):
        """
        Initialize the Input handler.
        
        Args:
            prompt: The prompt to display when asking for input
        """
        self.prompt = prompt
        self._input_type = str  # Default type
        self._validators: List[Callable[[Any], Tuple[bool, str]]] = []
        self._default = None
        self._allow_empty = False
        self._options = None  # For menu-like selection
        self._case_sensitive = True
        self._error_msg = "Invalid input. Please try again."
        self._path_type = None  # 'file', 'dir', or None for any path
        self._multiple = False  # Whether to allow multiple selections

    def type(self, input_type: Type) -> 'Input':
        """Set the expected input type."""
        self._input_type = input_type
        return self
    
    def path(self, path_type: Optional[str] = None) -> 'Input':
        """
        Configure the input to expect a path.
        
        Args:
            path_type: 'file' for files only, 'dir' for directories only, None for any path
        """
        self._input_type = Path
        self._path_type = path_type
        return self

    def default(self, default_value: Any) -> 'Input':
        """Set a default value that will be returned if input is empty."""
        self._default = default_value
        self._allow_empty = True
        return self

    def allow_empty(self, allow: bool = True) -> 'Input':
        """Set whether empty input is allowed."""
        self._allow_empty = allow
        return self

    def options(self, options: List[Any], case_sensitive: bool = False, multiple: bool = False) -> 'Input':
        """
        Set valid options for the input (creates a menu-like selection).
        
        Args:
            options: List of valid options
            case_sensitive: Whether option comparison should be case sensitive
            multiple: Whether to allow multiple selections
        """
        self._options = options
        self._case_sensitive = case_sensitive
        self._multiple = multiple
        return self

    def multiple(self, allow_multiple: bool = True) -> 'Input':
        """Set whether multiple selections are allowed (only applies when options are set)."""
        self._multiple = allow_multiple
        return self

    def validate(self, validator: Callable[[Any], Tuple[bool, str]]) -> 'Input':
        """
        Add a custom validation function.
        
        The validator should return a tuple of (is_valid, error_message)
        """
        self._validators.append(validator)
        return self

    def range(self, min_val: Optional[Union[int, float]] = None, 
              max_val: Optional[Union[int, float]] = None) -> 'Input':
        """Validate that a number falls within a specified range."""
        def number_range_validator(value):
            if min_val is not None and value < min_val:
                return False, f"Value must be at least {min_val}"
            if max_val is not None and value > max_val:
                return False, f"Value must be at most {max_val}"
            return True, ""
        
        self.validate(lambda x: number_range_validator(x))
        return self

    def pattern(self, regex_pattern: str, 
                error_msg: str = "Input doesn't match required pattern") -> 'Input':
        """Validate that a string matches a regex pattern."""
        def pattern_validator(value):
            if not re.match(regex_pattern, str(value)):
                return False, error_msg
            return True, ""
        
        self.validate(pattern_validator)
        return self

    def error_message(self, message: str) -> 'Input':
        """Set a custom error message for validation failures."""
        self._error_msg = message
        return self

    def get_input(self):
        """Get input from the user with validation.
        
        Returns:
            The validated user input converted to the appropriate type.
            For multiple selections, returns a list of selected options.
            
        Raises:
            KeyboardInterrupt: If user cancels input with Ctrl+C
            EOFError: If user cancels input with Ctrl+D (Unix) or Ctrl+Z+Enter (Windows)
        """
        while True:
            try:
                # Display prompt with default hint if available
                prompt = self.prompt
                if self._default is not None:
                    prompt += f" [{self._default}]"
                if self._multiple and self._options:
                    prompt += " (comma-separated for multiple selections)"
                prompt += ": "

                raw_input = input(prompt).strip()
                
                # Handle empty input
                if not raw_input:
                    if self._allow_empty:
                        return self._default
                    print("Input cannot be empty.")
                    continue

                # Handle multiple selections
                if self._multiple and self._options:
                    selections = [s.strip() for s in raw_input.split(',')]
                    selected_values = []
                    
                    for selection in selections:
                        # Convert type if needed
                        try:
                            if self._input_type is bool:
                                value = self._parse_bool(selection)
                            else:
                                value = self._input_type(selection)
                        except ValueError:
                            print(f"Invalid {self._input_type.__name__} value in selection.")
                            break
                            
                        # Check against options
                        if not self._case_sensitive and isinstance(value, str):
                            value_lower = value.lower()
                            option_found = False
                            for option in self._options:
                                if isinstance(option, str) and (option.lower() == value_lower):
                                    selected_values.append(option)  # Return the case-matched option
                                    option_found = True
                                    break
                            if not option_found:
                                print(f"Selection '{value}' must be one of: {', '.join(str(o) for o in self._options)}")
                                break
                        elif value not in self._options:
                            print(f"Selection '{value}' must be one of: {', '.join(str(o) for o in self._options)}")
                            break
                    else:
                        # All selections were valid
                        return selected_values
                    
                    continue

                # Single selection processing (original code)
                try:
                    if self._input_type is bool:
                        value = self._parse_bool(raw_input)
                    elif self._input_type is Path:
                        path = Path(raw_input)
                        if self._path_type == 'file' and not path.is_file():
                            raise ValueError("Path must be an existing file")
                        if self._path_type == 'dir' and not path.is_dir():
                            raise ValueError("Path must be an existing directory")
                        if self._path_type and not path.exists():
                            raise ValueError("Path does not exist")
                        value = path
                    else:
                        value = self._input_type(raw_input)
                except ValueError:
                    print(f"Invalid {self._input_type.__name__} value.")
                    continue

                if self._options is not None:
                    if not self._case_sensitive and isinstance(value, str):
                        value_lower = value.lower()
                        option_found = False
                        for option in self._options:
                            if isinstance(option, str) and (option.lower() == value_lower):
                                value = option  # Return the case-matched option
                                option_found = True
                                break
                        if not option_found:
                            print(f"Must be one of: {', '.join(str(o) for o in self._options)}")
                            continue
                    elif value not in self._options:
                        print(f"Must be one of: {', '.join(str(o) for o in self._options)}")
                        continue

                for validator in self._validators:
                    is_valid, error_msg = validator(value)
                    if not is_valid:
                        print(error_msg)
                        break
                else:  # No validation errors
                    return value

            except KeyboardInterrupt:
                print("\nInput cancelled by user.")
                raise
            except EOFError:
                print("\nInput cancelled by user.")
                raise

    def _parse_bool(self, value: str) -> bool:
        """Parse boolean values with flexible input options."""
        true_values = ['true', 't', 'yes', 'y', '1']
        false_values = ['false', 'f', 'no', 'n', '0']
        
        lower_val = value.lower()
        if lower_val in true_values:
            return True
        if lower_val in false_values:
            return False
        raise ValueError(f"Cannot convert '{value}' to boolean")

    @classmethod
    def integer(cls, prompt: str = "", 
                min_val: Optional[int] = None, 
                max_val: Optional[int] = None) -> int:
        """Convenience method for getting an integer with range validation."""
        return cls(prompt).type(int).range(min_val, max_val).get_input()

    @classmethod
    def float(cls, prompt: str = "", 
              min_val: Optional[float] = None, 
              max_val: Optional[float] = None) -> float:
        """Convenience method for getting a float with range validation."""
        return cls(prompt).type(float).range(min_val, max_val).get_input()

    @classmethod
    def string(cls, prompt: str = "", 
               pattern: Optional[str] = None,
               error_msg: Optional[str] = None) -> str:
        """Convenience method for getting a string with optional pattern validation."""
        input_obj = cls(prompt).type(str)
        if pattern:
            if error_msg:
                input_obj.pattern(pattern, error_msg)
            else:
                input_obj.pattern(pattern)
        return input_obj.get_input()

    @classmethod
    def boolean(cls, prompt: str = "") -> bool:
        """Convenience method for getting a boolean (accepts yes/no, true/false, etc.)."""
        return cls(prompt).type(bool).get_input()

    @classmethod
    def choice(cls, prompt: str = "", 
               options: List[Any] = [],
               case_sensitive: bool = False,
               multiple: bool = False) -> Any:
        """Convenience method for selecting from a list of options."""
        return cls(prompt).options(options, case_sensitive, multiple).get_input()
    
    @classmethod
    def file_path(cls, prompt: str = "", must_exist: bool = True) -> Path:
        """Convenience method for getting a file path."""
        input_obj = cls(prompt).path('file')
        if must_exist:
            input_obj.validate(lambda p: (p.exists() and p.is_file(), "File must exist"))
        return input_obj.get_input()

    @classmethod
    def dir_path(cls, prompt: str = "", must_exist: bool = True) -> Path:
        """Convenience method for getting a directory path."""
        input_obj = cls(prompt).path('dir')
        if must_exist:
            input_obj.validate(lambda p: (p.exists() and p.is_dir(), "Directory must exist"))
        return input_obj.get_input()
