import tkinter as tk
from tkinter import filedialog, messagebox

from converter import excel_to_csv


class ConverterUI:
    def __init__(self, root):
        self.root = root

        self.root.title("Excel CSV Converter")
        self.root.geometry("600x350")
        self.root.resizable(False, False)

        self.file_path = None
        self.log_box = None

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

    def create_widgets(self):
        # タイトル
        title = tk.Label(
            self.root,
            text="Excel CSV Converter",
            font=("Arial", 16)
        )
        title.pack(pady=20)

        # ファイルパス表示
        self.file_label = tk.Label(
            self.root,
            text="Excelファイルが選択されていません",
            wraplength=450
        )
        self.file_label.pack(pady=10)

        # Excel選択ボタン
        select_button = tk.Button(
            self.root,
            text="Excelを選択",
            command=self.select_file
        )
        select_button.pack(pady=10)

        # 変換ボタン
        self.convert_button = tk.Button(
            self.root,
            text="CSVへ変換",
            command=self.convert
        )

        self.convert_button.pack(
            pady=10
        )

        self.status_label = tk.Label(
            self.root,
            text=""
        )
        self.status_label.pack(pady=10)

        # ログ表示
        self.log_box = tk.Text(
            self.root,
            height=8,
            width=60
        )

        self.log_box.pack(
            pady=10
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

            excel_to_csv(
                self.file_path
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