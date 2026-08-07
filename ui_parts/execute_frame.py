import tkinter as tk


class ExecuteFrame:

    def __init__(self, parent, on_convert):

        self.on_convert = on_convert

        self.frame = tk.LabelFrame(
            parent,
            text="実行"
        )

        self.frame.pack(
            padx=10,
            pady=10,
            fill="x"
        )


        self.convert_button = tk.Button(
            self.frame,
            text="CSVへ変換",
            command=self.on_convert
        )

        self.convert_button.pack(
            pady=10
        )


        self.status_label = tk.Label(
            self.frame,
            text="待機中"
        )

        self.status_label.pack(
            pady=5
        )


    def set_status(self, text):

        self.status_label.config(
            text=text
        )


    def enable_button(self):

        self.convert_button.config(
            state="normal"
        )


    def disable_button(self):

        self.convert_button.config(
            state="disabled"
        )