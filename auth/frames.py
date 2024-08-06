from typing import TYPE_CHECKING
import customtkinter as ctk
from sqlalchemy import select
from admin.frames import MainFrame as AdminFrame
from customer.frames import MainFrame as CustomerFrame
from auth.models import User
from db import DB

if TYPE_CHECKING:
    from main import App


class MainFrame(ctk.CTkFrame):
    def __init__(self, parent: "App"):
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

    def login(self):
        session = DB.get_session()

        stmt = (
            select(User)
            .where(User.name == self.user_entry.get())
            .where(User.password == self.user_pass.get())
        )

        user = session.scalars(stmt).first()

        if user:
            if user.is_admin:
                self.parent.show_frame(AdminFrame)
            else:
                self.parent.show_frame(CustomerFrame)

        self.user_entry.delete(0, "end")
        self.user_pass.delete(0, "end")
