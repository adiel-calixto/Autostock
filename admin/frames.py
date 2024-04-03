from tkinter import ttk
import tkinter as tk
import customtkinter as ctk
from sqlalchemy import or_, select
from db import DB
from shared.models import Product


class Sidebar(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.grid_rowconfigure(4, weight=1)

        self.logo_label = ctk.CTkLabel(
            self, text="Autostock", font=ctk.CTkFont(size=20, weight="bold")
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = ctk.CTkButton(self, text="Adicionar produto")
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = ctk.CTkButton(self, text="Atualizar produto")
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = ctk.CTkButton(self, text="Remover produto")
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.appearance_mode_label = ctk.CTkLabel(
            self, text="Appearance Mode:", anchor="w"
        )
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(
            self,
            values=["System", "Light", "Dark"],
            command=self.change_appearance_mode_event,
        )
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = ctk.CTkLabel(self, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = ctk.CTkOptionMenu(
            self,
            values=["80%", "90%", "100%", "110%", "120%"],
            command=self.change_scaling_event,
        )
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)


class MainFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self._selected_product = None
        self._products = []

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.sidebar = Sidebar(self)
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")

        self.search_frame = ctk.CTkFrame(self)
        self.search_frame.grid_columnconfigure(0, weight=1)

        self.search_input = ctk.CTkEntry(self.search_frame, placeholder_text="Buscar")
        self.search_input.grid(row=0, column=0, sticky="nsew")

        self.search_button = ctk.CTkButton(
            self.search_frame, text="🔍", command=self._search_product, width=64
        )
        self.search_button.grid(row=0, column=1, padx=(10, 0))

        self.search_frame.grid(row=0, column=1, sticky="nsew", pady=10, padx=10)

        columns = ("id", "name", "price", "ref")

        self.table_frame = ctk.CTkScrollableFrame(self)
        self.table_frame.rowconfigure(0, weight=1)
        self.table_frame.columnconfigure(0, weight=1)

        self.table = ttk.Treeview(
            master=self.table_frame,
            columns=columns,
            show="headings",
        )

        self.table.column("#1", minwidth=50, width=50)
        self.table.column("#2", minwidth=220, width=220)
        self.table.column("#3", minwidth=120, width=120)
        self.table.column("#4", minwidth=120, width=120)

        self.table.heading("id", anchor="w", text="ID")
        self.table.heading("name", anchor="w", text="Nome")
        self.table.heading("price", anchor="w", text="Preço")
        self.table.heading("ref", anchor="w", text="Ref.")

        self.table.grid(row=0, column=0, sticky="nsew")
        self.table.bind("<<TreeviewSelect>>", self._item_selected)

        self.table_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        self.update_products()

    def _search_product(self):
        self.update_products(self.search_input.get())

    def _item_selected(self, event):
        selection = self.table.selection()

        if len(selection) > 0:
            self.selected_product = self.table.item(self.table.selection()[0])

    def _show_products(self):
        self.table.delete(*self.table.get_children())

        for p in self._products:
            self.table.insert("", tk.END, values=(p.id, p.name, p.price, p.ref))

    def get_selected_product(self):
        return self._selected_product

    def get_products(self):
        return self._products

    def update_products(self, filter=""):
        session = DB.get_session()
        stmt = select(Product).where(
            or_(Product.name.like(f"{filter}%"), Product.ref == filter)
        )

        self._products = session.scalars(stmt)
        self._show_products()
