import tkinter as tk
from tkinter import messagebox

from settings import load_settings, save_settings


class SettingUI:

    def __init__(self, parent, on_saved=None):

        self.window = tk.Toplevel(parent)

        self.window.title("設定")
        self.window.geometry("400x300")
        self.window.resizable(False, False)

        self.on_saved = on_saved

        self.settings = load_settings()

        self.create_widgets()


    def create_widgets(self):

        # 読み込み方法
        mode_label = tk.Label(
            self.window,
            text="読み込み方法"
        )

        mode_label.pack(
            pady=(20, 5)
        )


        self.mode = tk.StringVar(
            value=self.settings["default_mode"]
        )


        radio1 = tk.Radiobutton(
            self.window,
            text="購入内容が空白まで",
            variable=self.mode,
            value="1"
        )

        radio1.pack()


        radio2 = tk.Radiobutton(
            self.window,
            text="指定行まで",
            variable=self.mode,
            value="2"
        )

        radio2.pack()


        # 行数
        rows_label = tk.Label(
            self.window,
            text="読み込み行数"
        )

        rows_label.pack(
            pady=(10,0)
        )


        self.max_rows = tk.Entry(
            self.window
        )

        self.max_rows.insert(
            0,
            str(self.settings["default_max_rows"])
        )

        self.max_rows.pack()


        # 保存ボタン
        save_button = tk.Button(
            self.window,
            text="保存",
            command=self.save
        )

        save_button.pack(
            pady=20
        )

        # ZIP作成
        self.create_zip = tk.BooleanVar(
            value=self.settings["create_zip"]
        )

        zip_check = tk.Checkbutton(
            self.window,
            text="ZIPファイルを作成する",
            variable=self.create_zip
        )

        zip_check.pack(
            pady=10
        )


    def save(self):
        self.settings["default_mode"] = self.mode.get()
        try:
            max_rows = int(
                self.max_rows.get()
            )

            if max_rows <= 0:
                raise ValueError

        except ValueError:
            messagebox.showerror(
                "入力エラー",
                "読み込み行数には1以上の数字を入力してください"
            )
            return

        self.settings["default_max_rows"] = max_rows

        self.settings["create_zip"] = self.create_zip.get()

        save_settings(
            self.settings
        )

        messagebox.showinfo(
            "保存",
            "設定を保存しました"
        )

        if self.on_saved:
            self.on_saved()

        self.window.destroy()


if __name__ == "__main__":

    root = tk.Tk()

    root.withdraw()

    SettingUI(root)

    root.mainloop()