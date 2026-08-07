import tkinter as tk
from tkinter import filedialog, messagebox
import threading

from converter import excel_to_csv
from config import (
    APP_NAME,
    WINDOW_SIZE
)
from settings import load_settings
from setting_ui import SettingUI
from ui_parts.log_frame import LogFrame
from ui_parts.file_frame import FileFrame
from ui_parts.setting_frame import SettingFrame

class ConverterUI:
    def __init__(self, root):
        self.root = root

        self.root.title(APP_NAME)
        self.root.geometry(WINDOW_SIZE)
        self.root.resizable(False, False)

        self.file_path = None

        self.settings = load_settings()
        self.create_widgets()

    def add_log(self, message):

        self.root.after(
            0,
            self.log_frame.add_log,
            message
        )

    def create_widgets(self):
        # タイトル
        title = tk.Label(
            self.root,
            text="Excel CSV Converter",
            font=("Arial", 16)
        )

        title.pack(pady=20)

        setting_button = tk.Button(
                self.root,
                text="設定",
                command=self.open_settings
            )

        setting_button.pack(
            pady=5
        )

        self.file_frame = FileFrame(
            self.root,
            self.file_selected
        )
        self.setting_frame = SettingFrame(
            self.root,
            self.settings
        )
        self.create_execute_frame()
        self.log_frame = LogFrame(
            self.root
        )

    def file_selected(self, file_path):
        self.file_path = file_path

    # 設定画面を開く関数
    def open_settings(self):
        SettingUI(
            self.root,
            self.reload_settings
        )

    # 設定のメイン反映
    def reload_settings(self):
        self.settings = load_settings()

    # 実行・変換部分
    def create_execute_frame(self):
        execute_frame = tk.LabelFrame(
            self.root,
            text="実行"
        )

        execute_frame.pack(
            padx=10,
            pady=10,
            fill="x"
        )


        self.convert_button = tk.Button(
            execute_frame,
            text="CSVへ変換",
            command=self.convert
        )

        self.convert_button.pack(
            pady=10
        )


        self.status_label = tk.Label(
            execute_frame,
            text="待機中"
        )

        self.status_label.pack(
            pady=5
        )

    def convert(self):

        if not self.file_path:
            messagebox.showwarning(
                "警告",
                "Excelファイルを選択してください"
            )
            return

        self.convert_button.config(
            state="disabled"
        )

        self.status_label.config(
            text="変換中..."
        )

        self.add_log(
            "変換開始..."
        )

        self.root.update()

        values = self.setting_frame.get_values()

        mode = values["mode"]
        max_rows = values["max_rows"]

        threading.Thread(
            target=self.run_conversion,
            args=(mode, max_rows),
            daemon=True
        ).start()


    def run_conversion(self, mode, max_rows):
        try:
            excel_to_csv(
                self.file_path,
                mode=mode,
                max_rows=max_rows,
                log_callback=self.add_log
            )

            self.root.after(
                0,
                self.finish_conversion
            )

        except Exception as e:

            self.root.after(
                0,
                lambda: self.show_error(e)
            )


    def finish_conversion(self):
        self.add_log(
            "変換完了"
        )

        self.status_label.config(
            text="完了"
        )

        self.convert_button.config(
            state="normal"
        )

        messagebox.showinfo(
            "完了",
            "変換が完了しました"
        )


    def show_error(self, e):
        self.add_log(
            f"エラー: {e}"
        )

        self.convert_button.config(
            state="normal"
        )

        self.status_label.config(
            text="エラー"
        )

        messagebox.showerror(
            "エラー",
            str(e)
        )


def start_ui():
    root = tk.Tk()

    ConverterUI(root)

    root.mainloop()