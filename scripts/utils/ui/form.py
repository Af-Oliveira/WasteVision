"""
form.py - Dynamic Tkinter form generator for WasteVision

This module provides the FormGenerator class, which allows you to build
and display interactive forms using Tkinter. It supports various input types,
validation, default values, option selection (single and multiple), and
integration with the project's Input class for consistent user input handling.
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from typing import List, Dict, Any, Optional
from pathlib import Path
from scripts.utils.ui.input import Input

class FormGenerator:
    """
    Generates and manages a dynamic Tkinter form for user input.

    Features:
    - Add multiple input fields with validation and default values
    - Supports string, boolean, path, and option selection inputs
    - Handles single and multiple selections
    - Integrates with the Input class for consistent validation
    - Returns user input as a dictionary or None if cancelled
    """

    def __init__(self, title: str = "Form", window_width: int = 700, window_height: int = 600):
        """
        Initialize the form generator window.

        Args:
            title: The window title.
            window_width: Width of the form window.
            window_height: Height of the form window.
        """
        self.title = title
        self.window_width = window_width
        self.window_height = window_height
        self.input_specs: List[Input] = []
        self.input_widgets: Dict[str, Any] = {}
        self.result: Optional[Dict[str, Any]] = None
        self.root = tk.Tk()
        self.root.title(self.title)
        self.root.geometry(f"{self.window_width}x{self.window_height}")
        self.root.resizable(False, False)
        # Handle window close (X) button
        self.root.protocol("WM_DELETE_WINDOW", self._on_cancel)

    def add_input(self, input_spec: Input) -> 'FormGenerator':
        """
        Add an input specification to the form.

        Args:
            input_spec: An Input object describing the input field.

        Returns:
            self (for method chaining)
        """
        self.input_specs.append(input_spec)
        return self

    def show(self) -> Optional[Dict[str, Any]]:
        """
        Display the form and start the Tkinter main loop.

        Returns:
            dict: User input values if submitted, or None if cancelled.
        """
        self._create_form()
        self.root.mainloop()
        return self.result

    def _create_form(self):
        """
        Build the form UI with all input fields and action buttons.
        """
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Fill out the form:", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 10))

        for spec in self.input_specs:
            self._create_input_element(frame, spec)

        button_frame = ttk.Frame(frame)
        button_frame.pack(pady=20)

        ttk.Button(button_frame, text="Submit", width=20, command=self._on_submit).pack(side="left", padx=10)
        ttk.Button(button_frame, text="Cancel", width=20, command=self._on_cancel).pack(side="left", padx=10)

    def _create_input_element(self, parent, spec: Input):
        """
        Create and add a single input widget to the form based on the Input spec.

        Args:
            parent: The parent Tkinter widget.
            spec: The Input specification for this field.
        """
        container = ttk.LabelFrame(parent, text=spec.prompt, padding=(10, 5))
        container.pack(fill="x", pady=8)

        widget = None

        if spec._input_type is bool:
            # Boolean as Yes/No dropdown
            var = tk.StringVar(value="Yes")
            widget = ttk.Combobox(container, values=["Yes", "No"], textvariable=var, state="readonly")
            widget.pack(fill="x", padx=5)
            self.input_widgets[spec.prompt] = var

        elif spec._options is not None:
            # Option selection (single or multiple)
            if spec._multiple:
                listbox = tk.Listbox(container, selectmode=tk.MULTIPLE, height=min(10, len(spec._options)))
                for item in spec._options:
                    listbox.insert(tk.END, item)
                listbox.pack(fill="x", padx=5)
                self.input_widgets[spec.prompt] = listbox
            else:
                var = tk.StringVar(value=spec._default or spec._options[0])
                dropdown = ttk.Combobox(container, values=spec._options, textvariable=var, state="readonly")
                dropdown.pack(fill="x", padx=5)
                self.input_widgets[spec.prompt] = var

        elif spec._input_type is Path:
            # File or directory path input with browse button
            path_var = tk.StringVar(value=str(spec._default or ""))
            path_frame = ttk.Frame(container)
            path_frame.pack(fill="x", padx=5)

            entry = ttk.Entry(path_frame, textvariable=path_var)
            entry.pack(side="left", fill="x", expand=True)

            def browse():
                file_path = ""
                if spec._path_type == 'file':
                    file_path = filedialog.askopenfilename()
                elif spec._path_type == 'dir':
                    file_path = filedialog.askdirectory()
                if file_path:
                    path_var.set(file_path)

            ttk.Button(path_frame, text="Procurar", command=browse).pack(side="left", padx=5)
            self.input_widgets[spec.prompt] = path_var

        else:
            # Default: string input
            var = tk.StringVar(value=str(spec._default or ""))
            entry = ttk.Entry(container, textvariable=var)
            entry.pack(fill="x", padx=5)
            self.input_widgets[spec.prompt] = var

    def _on_submit(self):
        """
        Handle the submit button: validate inputs and close the form if valid.
        """
        values = {}
        for spec in self.input_specs:
            widget = self.input_widgets[spec.prompt]

            if isinstance(widget, tk.StringVar):
                values[spec.prompt] = widget.get()
            elif isinstance(widget, tk.Listbox):
                selected = [widget.get(i) for i in widget.curselection()]
                values[spec.prompt] = selected if selected else None
            else:
                values[spec.prompt] = widget.get()

        errors = self._validate_inputs(values)
        if errors:
            self._show_errors(errors)
        else:
            self.result = self._convert_values(values)
            self._close_window()

    def _on_cancel(self):
        """
        Handle the cancel button or window close event.
        """
        self.result = None
        self._close_window()

    def _close_window(self):
        """
        Close and destroy the Tkinter form window.
        """
        self.root.quit()
        self.root.destroy()

    def _validate_inputs(self, values: Dict[str, Any]) -> Dict[str, str]:
        """
        Validate all input values using the Input specs.

        Args:
            values: Dictionary of raw input values keyed by prompt.

        Returns:
            dict: Errors found, keyed by prompt.
        """
        errors = {}
        for spec in self.input_specs:
            value = values.get(spec.prompt, "")
            if value is None or (isinstance(value, str) and not value.strip()):
                if not spec._allow_empty:
                    errors[spec.prompt] = "Campo obrigatório"
                continue
            
            try:
                if spec._multiple and isinstance(value, list):
                    for item in value:
                        parsed = spec._parse_bool(item) if spec._input_type is bool else spec._input_type(item)
                        if spec._options and parsed not in spec._options:
                            raise ValueError()
                        for validator in spec._validators:
                            valid, msg = validator(parsed)
                            if not valid:
                                raise ValueError(msg)
                else:
                    parsed = spec._parse_bool(value) if spec._input_type is bool else spec._input_type(value)
                    if spec._options and parsed not in spec._options:
                        raise ValueError(f"Deve ser um dos seguintes: {', '.join(str(o) for o in spec._options)}")
                    for validator in spec._validators:
                        valid, msg = validator(parsed)
                        if not valid:
                            raise ValueError(msg)
            except ValueError as e:
                errors[spec.prompt] = str(e) or f"Valor inválido ({spec._input_type.__name__})"
        return errors

    def _convert_values(self, values: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert raw input values to their final types using the Input specs.

        Args:
            values: Dictionary of raw input values keyed by prompt.

        Returns:
            dict: Converted values keyed by prompt.
        """
        result = {}
        for spec in self.input_specs:
            value = values.get(spec.prompt)
            if value is None or (isinstance(value, str) and not value.strip()):
                result[spec.prompt] = spec._default
                continue
            if spec._multiple and isinstance(value, list):
                result[spec.prompt] = [spec._parse_bool(v) if spec._input_type is bool else spec._input_type(v)
                                   for v in value]
            else:
                result[spec.prompt] = spec._parse_bool(value) if spec._input_type is bool else spec._input_type(value)
        return result

    def _show_errors(self, errors: Dict[str, str]):
        """
        Display validation errors in a message box.

        Args:
            errors: Dictionary of error messages keyed by prompt.
        """
        message = "Corrija os seguintes erros:\n"
        message += "\n".join(f"- {key}: {msg}" for key, msg in errors.items())
        messagebox.showerror("Erros de Validação", message)