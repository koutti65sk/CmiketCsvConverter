import tkinter as tk
from tkinter import filedialog

from settings import save_settings


class OutputFrame:

    def __init__(self, parent, settings):

        self.settings = settings

        self.output_dir = settings.get(
            "last_output_dir",
            ""
        )

        if self.output_dir == "":
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

        if self.output_dir:
            display_path = self.output_dir
        else:
            display_path = "Excelと同じフォルダに保存"

        self.path_label = tk.Label(
            self.frame,
            text=display_path,
            wraplength=450
        )

        name_label = tk.Label(
            self.frame,
            text="保存する名前"
        )

        name_label.pack(
            pady=(10, 2)
        )

        self.name_entry = tk.Entry(
            self.frame,
            width=45
        )

        self.name_entry.pack(
            padx=10,
            pady=(0, 10)
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

        self.settings["last_output_dir"] = ""

        save_settings(
            self.settings
        )

        self.path_label.config(
            text="Excelと同じフォルダに保存"
        )

    def get_output_dir(self):

        return self.output_dir

    def select_folder(self):

        folder_path = filedialog.askdirectory(
            title="保存先フォルダを選択"
        )

        if folder_path:

            self.output_dir = folder_path

            self.settings["last_output_dir"] = folder_path

            save_settings(
                self.settings
            )

            self.path_label.config(
                text=folder_path
            )

    def get_output_name(self):

        name = self.name_entry.get().strip()

        return name