import tkinter as tk


class SettingFrame:

    def __init__(self, parent, settings):

        self.settings = settings

        self.frame = tk.LabelFrame(
            parent,
            text="変換設定"
        )

        self.frame.pack(
            padx=10,
            pady=10,
            fill="x"
        )


        self.mode = tk.StringVar(
            value=self.settings["default_mode"]
        )


        mode_label = tk.Label(
            self.frame,
            text="読み込み方法"
        )

        mode_label.pack(
            pady=(10, 0)
        )


        radio1 = tk.Radiobutton(
            self.frame,
            text="購入内容が空白まで",
            variable=self.mode,
            value="1",
            command=self.change_mode
        )

        radio1.pack()


        radio2 = tk.Radiobutton(
            self.frame,
            text="指定行まで",
            variable=self.mode,
            value="2",
            command=self.change_mode
        )

        radio2.pack()


        self.max_rows = tk.Entry(
            self.frame,
            width=10
        )


        self.max_rows.insert(
            0,
            str(self.settings["default_max_rows"])
        )

        self.max_rows.pack()


        self.change_mode()


    def change_mode(self):

        if self.mode.get() == "1":

            self.max_rows.config(
                state="disabled"
            )

        else:

            self.max_rows.config(
                state="normal"
            )


    def get_values(self):

        if self.mode.get() == "2":

            max_rows = int(
                self.max_rows.get()
            )

        else:

            max_rows = None


        return {
            "mode": self.mode.get(),
            "max_rows": max_rows
        }