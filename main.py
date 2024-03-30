import customtkinter as ctk
from db import DB
from frames import AutoFrame, AdminFrame, LoginFrame


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Test")
        self.geometry("640x480")
        self.resizable(False, False)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frames = {}

        for F in (AutoFrame, AdminFrame, LoginFrame):
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
    app.mainloop()

    DB.close_conn()
