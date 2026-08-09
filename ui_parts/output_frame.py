import tkinter as tk
from tkinter import filedialog


class OutputFrame:

    def __init__(self, parent):

        self.output_dir = None

        self.frame = tk.LabelFrame(
            parent,
            text="保存先"
        )

        self.frame.pack(
            padx=10,
            pady=5,
            fill="x"
        )

        self.path_label = tk.Label(
            self.frame,
            text="Excelと同じフォルダに保存",
            wraplength=450
        )

        self.path_label.pack(
            padx=10,
            pady=5
        )

        button_frame = tk.Frame(
            self.frame
        )

        button_frame.pack(
            pady=5
        )

        select_button = tk.Button(
            button_frame,
            text="保存先を選択",
            command=self.select_folder
        )

        select_button.pack(
            side="left",
            padx=5
        )

        reset_button = tk.Button(
            button_frame,
            text="元に戻す",
            command=self.reset
        )

        reset_button.pack(
            side="left",
            padx=5
        )

    def select_folder(self):

        folder_path = filedialog.askdirectory(
            title="保存先フォルダを選択"
        )

        if folder_path:

            self.output_dir = folder_path

            self.path_label.config(
                text=folder_path
            )

    def reset(self):

        self.output_dir = None

        self.path_label.config(
            text="Excelと同じフォルダに保存"
        )

    def get_output_dir(self):

        return self.output_dir