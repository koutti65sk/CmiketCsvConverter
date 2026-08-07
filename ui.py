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

class ConverterUI:
    def __init__(self, root):
        self.root = root

        self.root.title(APP_NAME)
        self.root.geometry(WINDOW_SIZE)
        self.root.resizable(False, False)

        self.file_path = None
        self.log_box = None

        self.settings = load_settings()

        self.mode = tk.StringVar(
            value=self.settings["default_mode"]
        )
        self.create_widgets()

    def add_log(self, message):

        self.root.after(
            0,
            self.log_frame.add_log,
            message
        )


    def _add_log(self, message):

        self.log_box.insert(
            tk.END,
            message + "\n"
        )

        self.log_box.see(
            tk.END
        )

    def change_mode(self):

        if self.mode.get() == "1":

            self.max_rows.config(
                state="disabled"
            )

        else:

            self.max_rows.config(
                state="normal"
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

        self.create_file_frame()
        self.create_setting_frame()
        self.create_execute_frame()
        self.log_frame = LogFrame(
            self.root
        )


    # ファイル選択部分
    def create_file_frame(self):
        file_frame = tk.LabelFrame(
            self.root,
            text="ファイル選択"
        )

        file_frame.pack(
            padx=10,
            pady=10,
            fill="x"
        )

        self.file_label = tk.Label(
            file_frame,
            text="Excelファイルが選択されていません",
            wraplength=450
        )

        self.file_label.pack(
            padx=10,
            pady=5
        )

        select_button = tk.Button(
            file_frame,
            text="Excelを選択",
            command=self.select_file
        )

        select_button.pack(
            pady=5
        )

    # 変換設定部分
    def create_setting_frame(self):
        setting_frame = tk.LabelFrame(
            self.root,
            text="変換設定"
        )

        setting_frame.pack(
            padx=10,
            pady=10,
            fill="x"
        )

        mode_label = tk.Label(
            setting_frame,
            text="読み込み方法"
        )

        mode_label.pack(
            pady=(10, 0)
        )


        radio1 = tk.Radiobutton(
            setting_frame,
            text="購入内容が空白まで",
            variable=self.mode,
            value="1",
            command=self.change_mode
        )

        radio1.pack()


        radio2 = tk.Radiobutton(
            setting_frame,
            text="指定行まで",
            variable=self.mode,
            value="2",
            command=self.change_mode
        )

        radio2.pack()


        self.max_rows = tk.Entry(
            setting_frame,
            width=10
        )

        self.max_rows.insert(
            0,
            str(self.settings["default_max_rows"])
        )

        self.max_rows.pack()


        self.change_mode()

    # 設定画面を開く関数
    def open_settings(self):
        SettingUI(
            self.root,
            self.reload_settings
        )

    # 設定のメイン反映
    def reload_settings(self):

        self.settings = load_settings()

        self.mode.set(
            self.settings["default_mode"]
        )

        self.max_rows.delete(
            0,
            tk.END
        )

        self.max_rows.insert(
            0,
            str(self.settings["default_max_rows"])
        )

        self.change_mode()

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


    def select_file(self):
        file_path = filedialog.askopenfilename(
            title="変換するExcelファイルを選択",
            filetypes=[
                ("Excelファイル", "*.xlsx"),
                ("Excelファイル", "*.xls")
            ]
        )

        if file_path:
            self.file_path = file_path
            self.file_label.config(
                text=file_path
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

        if self.mode.get() == "2":
            max_rows = int(self.max_rows.get())
        else:
            max_rows = None


        threading.Thread(
            target=self.run_conversion,
            args=(max_rows,),
            daemon=True
        ).start()


    def run_conversion(self, max_rows):
        try:
            excel_to_csv(
                self.file_path,
                mode=self.mode.get(),
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