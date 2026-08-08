import tkinter as tk


class ExecuteFrame:

    def __init__(
        self,
        parent,
        on_convert,
        on_open_folder,
        on_cancel
    ):

        self.on_convert = on_convert
        self.on_open_folder = on_open_folder
        self.on_cancel = on_cancel

        self.on_open_folder = on_open_folder

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

        self.cancel_button = tk.Button(
            self.frame,
            text="変換をキャンセル",
            command=self.on_cancel
        )

        self.cancel_button.pack(
            pady=5
        )

        self.cancel_button.config(
            state="disabled"
)

        self.open_folder_button = tk.Button(
            self.frame,
            text="出力フォルダを開く",
            command=self.on_open_folder
        )

        self.open_folder_button.pack(
            pady=5
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

        self.open_folder_button.config(
            state="normal"
        )


    def disable_button(self):

        self.convert_button.config(
            state="disabled"
        )

        self.open_folder_button.config(
            state="disabled"
        )

    def enable_cancel_button(self):

        self.cancel_button.config(
            state="normal"
        )


    def disable_cancel_button(self):

        self.cancel_button.config(
            state="disabled"
        )