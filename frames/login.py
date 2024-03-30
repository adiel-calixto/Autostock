import customtkinter as ctk
from frames.admin import AdminFrame
from frames.auto import AutoFrame


class LoginFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        label = ctk.CTkLabel(self, text="Insira suas credenciais")
        label.pack(pady=10, padx=10)

        # Create the text box for taking
        # username input from user
        self.user_entry = ctk.CTkEntry(self, placeholder_text="Nome")
        self.user_entry.pack(pady=8, padx=10)

        # Create a text box for taking
        # password input from user
        self.user_pass = ctk.CTkEntry(self, placeholder_text="Senha", show="*")
        self.user_pass.pack(pady=8, padx=10)

        # Create a login button to login
        self.button = ctk.CTkButton(self, text="Entrar", command=self.login)
        self.button.pack(pady=8, padx=10)

        # Create a remember me checkbox
        self.checkbox = ctk.CTkCheckBox(self, text="Abrir caixa?")
        self.checkbox.pack(pady=10, padx=10)

    def login(self):
        # ToDo: Mover essas credenciais para outro lugar
        username = "admin"
        password = "admin"

        if self.user_entry.get() == username and self.user_pass.get() == password:
            if bool(self.checkbox.get()):
                self.parent.show_frame(AutoFrame)
            else:
                self.parent.show_frame(AdminFrame)

        self.user_entry.delete(0, "end")
        self.user_pass.delete(0, "end")
