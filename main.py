from tkinter import ttk
import customtkinter as ctk
from auth.frames import MainFrame as LoginFrame
from admin.frames import MainFrame as AdminFrame
from customer.frames import MainFrame as CustomerFrame
from shared.utils import import_models


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Test")
        self.geometry("840x540")
        self.resizable(False, False)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        style = ttk.Style(self)
        style.theme_use("default")

        style.configure(
            "Treeview",
            background="#2a2b2b",
            foreground="white",
            rowheight=25,
            fieldbackground="#343637",
            bordercolor="#343637",
            borderwidth=0,
        )
        style.map("Treeview", background=[("selected", "#154970")])

        style.configure(
            "Treeview.Heading", background="#3b3b3b", foreground="white", relief="flat"
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

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


if __name__ == "__main__":
    app = App()
    import_models()
    app.mainloop()
