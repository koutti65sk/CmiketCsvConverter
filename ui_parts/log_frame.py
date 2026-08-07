import tkinter as tk


class LogFrame:

    def __init__(self, parent):

        self.frame = tk.LabelFrame(
            parent,
            text="ログ"
        )

        self.frame.pack(
            padx=10,
            pady=(0, 5),
            fill="both",
            expand=True
        )


        self.log_box = tk.Text(
            self.frame,
            height=15,
            width=70
        )


        scrollbar = tk.Scrollbar(
            self.frame,
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


    def add_log(self, message):

        self.log_box.insert(
            tk.END,
            message + "\n"
        )

        self.log_box.see(
            tk.END
        )