import tkinter as tk
from tkinter import ttk


class ProgressFrame:

    def __init__(self, parent):
        self.frame = tk.Frame(parent)

        self.progress = ttk.Progressbar(
            self.frame,
            orient="horizontal",
            length=400,
            mode="determinate"
        )

        self.progress.pack(
            pady=5
        )

        self.label = tk.Label(
            self.frame,
            text="0%"
        )

        self.label.pack(
            pady=2
        )

        self.frame.pack(
            pady=5
        )

    def set_progress(self, current, total):

        if total <= 0:
            return

        percent = int(
            current / total * 100
        )

        self.progress["value"] = percent

        self.label.config(
            text=f"{percent}%"
        )

    def reset(self):

        self.progress["value"] = 0

        self.label.config(
            text="0%"
        )