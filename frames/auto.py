import customtkinter as ctk


class AutoFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        label = ctk.CTkLabel(self, text="Auto atendimento")
        label.pack()
