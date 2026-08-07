import tkinter as tk
from tkinter import filedialog, messagebox

from converter import excel_to_csv
from config import (
    APP_NAME,
    WINDOW_SIZE
)
from settings import load_settings

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
        self.log_box.insert(
            tk.END,
            message + "\n"
        )

        self.log_box.see(
            tk.END
        )

        self.root.update()

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

        self.create_file_frame()
        self.create_setting_frame()
        self.create_execute_frame()
        self.create_log_frame()


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

    # ログ出力部分
    def create_log_frame(self):
        log_frame = tk.LabelFrame(
            self.root,
            text="ログ"
        )

        log_frame.pack(
            padx=10,
            pady=(0, 5),
            fill="both",
            expand=True
        )


        self.log_box = tk.Text(
            log_frame,
            height=15,
            width=70
        )


        scrollbar = tk.Scrollbar(
            log_frame,
            command=self.log_box.yview
        )


        self.log_box.configure(
            yscrollcommand=scrollbar.set
        )


        scrollbar.pack(
            side="right",
            fill="y"
        )


        self.log_box.pack(
            padx=5,
            pady=5,
            fill="both",
            expand=True
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

        try:

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

            excel_to_csv(
                self.file_path,
                mode=self.mode.get(),
                max_rows=max_rows,
                log_callback=self.add_log
            )

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

        except Exception as e:

            self.convert_button.config(
                state="normal"
            )

            self.add_log(
                f"エラー: {e}"
            )

            messagebox.showerror(
                "エラー",
                str(e)
            )


def start_ui():
    root = tk.Tk()

    app = ConverterUI(root)

    root.mainloop()