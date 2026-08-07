import tkinter as tk
from tkinter import filedialog


class FileFrame:

    def __init__(self, parent, on_selected):

        self.on_selected = on_selected

        self.frame = tk.LabelFrame(
            parent,
            text="ファイル選択"
        )

        self.frame.pack(
            padx=10,
            pady=10,
            fill="x"
        )


        self.file_label = tk.Label(
            self.frame,
            text="Excelファイルが選択されていません",
            wraplength=450
        )

        self.file_label.pack(
            padx=10,
            pady=5
        )


        select_button = tk.Button(
            self.frame,
            text="Excelを選択",
            command=self.select_file
        )

        select_button.pack(
            pady=5
        )


    def select_file(self):

        file_path = filedialog.askopenfilename(
            title="変換するExcelファイルを選択",
            filetypes=[
                ("Excelファイル", "*.xlsx"),
                ("Excelファイル", "*.xls")
            ]
        )


        if file_path:

            self.file_label.config(
                text=file_path
            )

            self.on_selected(file_path)