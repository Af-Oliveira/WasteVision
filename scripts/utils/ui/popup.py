import tkinter as tk
from tkinter import font as tkfont
from typing import Optional


class PopupManager:
    def __init__(self):
        self.result: Optional[bool] = None

    def _center_window(self, root, width, height):
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        root.geometry(f"{width}x{height}+{x}+{y}")

    def _print_console_box(self, title: str, message: str):
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
        self.show_message(title, message, width, height, consoleprompt)

    def show_confirm(self, title: str, message: str, width: int = 300, height: int = 100, consoleprompt: bool = False) -> Optional[bool]:
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
        popup = PopupManager()
        popup.show_message(title, message, consoleprompt=consoleprompt)

    @staticmethod
    def quick_confirm(title: str, message: str, consoleprompt: bool = False) -> Optional[bool]:
        popup = PopupManager()
        return popup.show_confirm(title, message, consoleprompt=consoleprompt)
