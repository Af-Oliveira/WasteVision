"""
popup.py - Popup and console message utilities for WasteVision

This module provides the PopupManager class, which allows you to display
informational, alert, and confirmation dialogs in both GUI (Tkinter) and
console environments. It is used throughout the project to provide user
feedback, confirmations, and alerts in a consistent and user-friendly way.
"""

import tkinter as tk
from tkinter import font as tkfont
from typing import Optional

class PopupManager:
    """
    Manages popup dialogs and console messages for user interaction.
    Supports both GUI (Tkinter) and console-based prompts.
    """

    def __init__(self):
        self.result: Optional[bool] = None

    def _center_window(self, root, width, height):
        """
        Center a Tkinter window on the screen.

        Args:
            root: The Tkinter root window.
            width: Desired window width.
            height: Desired window height.
        """
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        root.geometry(f"{width}x{height}+{x}+{y}")

    def _print_console_box(self, title: str, message: str):
        """
        Print a nicely formatted message box to the console.

        Args:
            title: The title of the message box.
            message: The message content.
        """
        border = "+" + "-" * 60 + "+"
        lines = [line.strip() for line in message.split("\n")]
        print(f"\n{border}")
        print(f"| {title.center(58)} |")
        print(f"|{'-' * 60}|")
        for line in lines:
            while len(line) > 58:
                print(f"| {line[:58]} |")
                line = line[58:]
            print(f"| {line.ljust(58)} |")
        print(f"{border}\n")

    def show_message(self, title: str, message: str, width: int = 300, height: int = 100, consoleprompt: bool = False):
        """
        Show an informational message to the user, either as a GUI popup or in the console.

        Args:
            title: The title of the message box.
            message: The message content.
            width: Width of the popup window (GUI only).
            height: Height of the popup window (GUI only).
            consoleprompt: If True, print to console instead of showing a GUI popup.
        """
        if consoleprompt:
            self._print_console_box(title, message)
            

        root = tk.Tk()
        root.title(title)
        self._center_window(root, width, height)
        root.configure(bg="#f0f2f5")
        root.resizable(False, False)

        body_font = tkfont.Font(family="Helvetica", size=11)

        frame = tk.Frame(root, bg="#f0f2f5", padx=20, pady=20)
        frame.pack(expand=True, fill='both')

        label = tk.Label(frame, text=message, wraplength=width - 40, bg="#f0f2f5", font=body_font, justify="center")
        label.pack(pady=(0, 20))

        ok_button = tk.Button(frame, text="OK", command=root.destroy, bg="#4CAF50", fg="white", padx=10, pady=5)
        ok_button.pack()

        root.mainloop()

    def show_alert(self, title: str, message: str, width: int = 300, height: int = 100, consoleprompt: bool = False):
        """
        Show an alert message to the user (alias for show_message).

        Args:
            title: The title of the alert.
            message: The alert content.
            width: Width of the popup window (GUI only).
            height: Height of the popup window (GUI only).
            consoleprompt: If True, print to console instead of showing a GUI popup.
        """
        self.show_message(title, message, width, height, consoleprompt)

    def show_confirm(self, title: str, message: str, width: int = 300, height: int = 100, consoleprompt: bool = False) -> Optional[bool]:
        """
        Show a confirmation dialog (Yes/No) to the user, either as a GUI popup or in the console.

        Args:
            title: The title of the confirmation dialog.
            message: The confirmation message.
            width: Width of the popup window (GUI only).
            height: Height of the popup window (GUI only).
            consoleprompt: If True, prompt in the console instead of showing a GUI popup.

        Returns:
            bool or None: True if user confirms, False if user declines, None if cancelled.
        """
        if consoleprompt:
            self._print_console_box(title, message)
            while True:
                response = input("Confirm [y/n]: ").strip().lower()
                if response in ['y', 'yes']:
                    return True
                elif response in ['n', 'no']:
                    return False
                print("Invalid input. Please enter 'y' or 'n'.")
            return None

        self.result = None
        root = tk.Tk()
        root.title(title)
        self._center_window(root, width, height)
        root.configure(bg="#f0f2f5")
        root.resizable(False, False)

        body_font = tkfont.Font(family="Helvetica", size=11)

        frame = tk.Frame(root, bg="#f0f2f5", padx=20, pady=20)
        frame.pack(expand=True, fill='both')

        label = tk.Label(frame, text=message, wraplength=width - 40, bg="#f0f2f5", font=body_font, justify="center")
        label.pack(pady=(0, 20))

        button_frame = tk.Frame(frame, bg="#f0f2f5")
        button_frame.pack()

        def on_yes():
            self.result = True
            root.destroy()

        def on_no():
            self.result = False
            root.destroy()

        yes_button = tk.Button(button_frame, text="Yes", command=on_yes,
                               bg="#4CAF50", fg="white", width=10, padx=5, pady=5)
        yes_button.pack(side="left", padx=10)

        no_button = tk.Button(button_frame, text="No", command=on_no,
                              bg="#f44336", fg="white", width=10, padx=5, pady=5)
        no_button.pack(side="left", padx=10)

        root.mainloop()
        return self.result

    @staticmethod
    def quick_message(title: str, message: str, consoleprompt: bool = False):
        """
        Quickly show an informational message using a temporary PopupManager instance.

        Args:
            title: The title of the message.
            message: The message content.
            consoleprompt: If True, print to console instead of showing a GUI popup.
        """
        popup = PopupManager()
        popup.show_message(title, message, consoleprompt=consoleprompt)

    @staticmethod
    def quick_confirm(title: str, message: str, consoleprompt: bool = False) -> Optional[bool]:
        """
        Quickly show a confirmation dialog using a temporary PopupManager instance.

        Args:
            title: The title of the confirmation dialog.
            message: The confirmation message.
            consoleprompt: If True, prompt in the console instead of showing a GUI popup.

        Returns:
            bool or None: True if user confirms, False if user declines, None if cancelled.
        """
        popup = PopupManager()
        return popup.show_confirm(title, message, consoleprompt=consoleprompt)
