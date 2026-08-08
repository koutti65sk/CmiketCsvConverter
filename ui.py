import tkinter as tk
from tkinter import messagebox
import threading
import os
from pathlib import Path

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
from ui_parts.execute_frame import ExecuteFrame
from ui_parts.progress_frame import ProgressFrame

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

        self.setting_button = tk.Button(
                self.root,
                text="設定",
                command=self.open_settings
            )

        self.setting_button.pack(
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
        self.progress_frame = ProgressFrame(
            self.root
        )
        self.execute_frame = ExecuteFrame(
            self.root,
            self.convert,
            self.open_output_folder
        )
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

        self.setting_frame.mode.set(
            self.settings["default_mode"]
        )

        self.setting_frame.max_rows.config(
            state="normal"
        )

        self.setting_frame.max_rows.delete(
            0,
            tk.END
        )

        self.setting_frame.max_rows.insert(
            0,
            str(self.settings["default_max_rows"])
        )

        self.setting_frame.create_zip.set(
            self.settings["create_zip"]
        )

        self.setting_frame.change_mode()

    def convert(self):
        if not self.file_path:
            messagebox.showwarning(
                "警告",
                "Excelファイルを選択してください"
            )
            return

        self.execute_frame.disable_button()

        self.file_frame.disable()

        self.setting_button.config(
            state="disabled"
        )

        self.execute_frame.set_status(
            "変換中..."
        )

        self.progress_frame.reset()

        self.add_log(
            "変換開始..."
        )

        self.root.update()

        values = self.setting_frame.get_values()

        mode = values["mode"]
        max_rows = values["max_rows"]
        create_zip = values["create_zip"]

        threading.Thread(
            target=self.run_conversion,
            args=(mode, max_rows, create_zip),
            daemon=True
        ).start()

    def open_output_folder(self):
        if not self.file_path:
            messagebox.showwarning(
                "警告",
                "Excelファイルを選択してください"
            )
            return

        output_dir = Path(
            self.file_path
        ).parent

        os.startfile(
            output_dir
        )


    def run_conversion(self, mode, max_rows, create_zip):
        try:
            excel_to_csv(
                self.file_path,
                mode=mode,
                max_rows=max_rows,
                create_zip=create_zip,
                log_callback=self.add_log,
                progress_callback=self.update_progress
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

        self.execute_frame.set_status(
            "完了"
        )

        self.execute_frame.enable_button()

        self.file_frame.enable()

        self.setting_button.config(
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

        self.execute_frame.enable_button()

        self.file_frame.enable()

        self.execute_frame.set_status(
            "エラー"
        )

        messagebox.showerror(
            "エラー",
            str(e)
        )


    def update_progress(self, current, total):

        self.root.after(
            0,
            self.progress_frame.set_progress,
            current,
            total
        )


def start_ui():
    root = tk.Tk()

    ConverterUI(root)

    root.mainloop()