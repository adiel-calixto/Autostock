from tkinter import ttk
from typing import Type, Union
import customtkinter as ctk
from auth.frames import MainFrame as LoginFrame
from admin.frames import MainFrame as AdminFrame
from customer.frames import MainFrame as CustomerFrame
from shared.utils import import_models

ctk.set_appearance_mode("Dark")
ctk.set_widget_scaling(1.5)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Test")
        self.geometry("1280x720")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        style = ttk.Style(self)
        style.theme_use("default")

        style.configure(
            "Treeview",
            background="#2a2b2b",
            foreground="white",
            rowheight=40,
            fieldbackground="#343637",
            bordercolor="#343637",
            borderwidth=0,
            font=(None, 14),
        )
        style.map("Treeview", background=[("selected", "#154970")])

        style.configure(
            "Treeview.Heading",
            background="#3b3b3b",
            foreground="white",
            relief="flat",
            font=(None, 16),
        )
        style.map("Treeview.Heading", background=[("active", "#206aa5")])

        self.frames = {}

        for F in (CustomerFrame, AdminFrame, LoginFrame):
            frame = F(self)
            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.bind("<Control-a>", self.__open_admin_callback)
        self.show_frame(LoginFrame)

    def __open_admin_callback(self, event):
        self.show_frame(LoginFrame)

    def show_frame(self, cont: Type[Union[AdminFrame, LoginFrame, CustomerFrame]]):
        frame = self.frames[cont]
        frame.tkraise()


if __name__ == "__main__":
    app = App()
    import_models()
    app.mainloop()
