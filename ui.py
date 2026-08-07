import tkinter as tk
from tkinter import filedialog, messagebox

from converter import excel_to_csv


class ConverterUI:
    def __init__(self, root):
        self.root = root

        self.root.title("Excel CSV Converter")
        self.root.geometry("600x550")
        self.root.resizable(False, False)

        self.file_path = None
        self.log_box = None

        self.mode = tk.StringVar(value="1")
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

        # ラベルを追加
        mode_label = tk.Label(
            self.root,
            text="読み込み方法"
        )

        mode_label.pack(pady=(10, 0))

        # ラジオボタン1の追加
        radio1 = tk.Radiobutton(
            self.root,
            text="購入内容が空白まで",
            variable=self.mode,
            value="1",
            command=self.change_mode
        )

        radio1.pack()

        # ラジオボタン2の追加
        radio2 = tk.Radiobutton(
            self.root,
            text="指定行まで",
            variable=self.mode,
            value="2",
            command=self.change_mode
        )

        radio2.pack()

        # ラジオボタン2のテキスト追加
        self.max_rows = tk.Entry(
            self.root,
            width=10
        )

        self.max_rows.insert(
            0,
            "1000"
        )

        self.max_rows.pack()
        self.change_mode()

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
        log_frame = tk.Frame(self.root)
        log_frame.pack(pady=10)

        self.log_box = tk.Text(
            self.root,
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

        self.log_box.pack(
            side="left"
        )

        scrollbar.pack(
            side="right",
            fill="y"
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

            print(self.mode.get())
            print(self.max_rows.get())

            if self.mode.get() == "2":
                max_rows = int(self.max_rows.get())
            else:
                max_rows = None

            excel_to_csv(
                self.file_path,
                mode=self.mode.get(),
                max_rows=max_rows
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