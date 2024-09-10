from datetime import date, timedelta
from tkinter import ttk
from tkinter.messagebox import askyesno
import tkinter as tk
from typing import TYPE_CHECKING
import customtkinter as ctk
from sqlalchemy import and_, delete, or_, select, text, update
from db import DB
from shared.models import Order, Product

if TYPE_CHECKING:
    from main import App


class MainFrame(ctk.CTkFrame):
    class UpdateWindow(ctk.CTkToplevel):
        def __init__(self, master: "MainFrame.Sidebar", callback, product):
            super().__init__(master)
            self.geometry("640x480")

            self.callback = callback
            self.product = product

            name_label = ctk.CTkLabel(self, text="Nome:")
            name_label.pack(pady=(20, 0))
            self.name_entry = ctk.CTkEntry(self, placeholder_text="Nome", width=360)
            self.name_entry.insert(0, product[1])
            self.name_entry.pack()

            ref_label = ctk.CTkLabel(self, text="Ref.:")
            ref_label.pack()
            self.ref_entry = ctk.CTkEntry(self, placeholder_text="Ref.", width=360)
            self.ref_entry.insert(0, product[3])
            self.ref_entry.pack()

            price_label = ctk.CTkLabel(self, text="Preço:")
            price_label.pack()
            self.price_entry = ctk.CTkEntry(self, placeholder_text="Preço", width=360)
            self.price_entry.insert(0, product[2])
            self.price_entry.pack()

            quantity_label = ctk.CTkLabel(self, text="Quantidade:")
            quantity_label.pack()
            self.quantity_entry = ctk.CTkEntry(self, placeholder_text="Quantidade", width=360)
            self.quantity_entry.insert(0, product[4])
            self.quantity_entry.pack()

            self.button = ctk.CTkButton(self, text="Salvar", command=self.update_product)
            self.button.pack(pady=20)

        def update_product(self):
            id = self.product[0]
            session = DB.get_session()

            stmt = (
                update(Product)
                .where(Product.id == id)
                .values(
                    name=self.name_entry.get(),
                    ref=self.ref_entry.get(),
                    price=self.price_entry.get(),
                    quantity=self.quantity_entry.get(),
                )
            )

            session.execute(stmt)
            session.commit()

            self.callback()
            self.destroy()

    class AddWindow(ctk.CTkToplevel):
        def __init__(self, master: "MainFrame.Sidebar", callback):
            super().__init__(master)

            self.geometry("640x480")
            self.callback = callback

            name_label = ctk.CTkLabel(self, text="Nome:")
            name_label.pack(pady=(20, 0))
            self.name_entry = ctk.CTkEntry(self, placeholder_text="Nome", width=360)
            self.name_entry.pack()

            ref_label = ctk.CTkLabel(self, text="Ref.:")
            ref_label.pack()
            self.ref_entry = ctk.CTkEntry(self, placeholder_text="Ref.", width=360)
            self.ref_entry.pack()

            price_label = ctk.CTkLabel(self, text="Preço:")
            price_label.pack()
            self.price_entry = ctk.CTkEntry(self, placeholder_text="Preço", width=360)
            self.price_entry.pack()

            quantity_label = ctk.CTkLabel(self, text="Quantidade:")
            quantity_label.pack()
            self.quantity_entry = ctk.CTkEntry(self, placeholder_text="Quantidade", width=360)
            self.quantity_entry.pack()

            self.button = ctk.CTkButton(self, text="Salvar", command=self.add_product)
            self.button.pack(pady=20)

        def add_product(self):
            product = Product(
                name=self.name_entry.get(),
                ref=self.ref_entry.get(),
                price=self.price_entry.get(),
                quantity=self.quantity_entry.get(),
                user_id=1,
            )
            session = DB.get_session()

            session.add(product)
            session.commit()

            self.callback()
            self.destroy()

    class OrdersWindow(ctk.CTkToplevel):
        def __init__(self, master: "MainFrame.Sidebar", callback):
            super().__init__(master)

            self.geometry("800x480")
            self.callback = callback

            session = DB.get_session()
            orders = session.query(Order).filter(Order.created_at > (date.today() - timedelta(days=1))).all()
            columns = ("id", "price", "payment", "products", "time")

            order_price = lambda order: sum([product.t_price * product.quantity for product in order.products])

            self.table = ttk.Treeview(
                master=self,
                columns=columns,
                show="headings",
            )

            self.table.column("#1", minwidth=50, width=50)
            self.table.column("#2", minwidth=100, width=100)
            self.table.column("#3", minwidth=150, width=150)
            self.table.column("#4", minwidth=320, width=320)
            self.table.column("#5", minwidth=100, width=100)

            self.table.heading("id", anchor="w", text="ID")
            self.table.heading("price", anchor="w", text="Valor")
            self.table.heading("payment", anchor="w", text="Pagamento")
            self.table.heading("products", anchor="w", text="Produtos")
            self.table.heading("time", anchor="w", text="Hora")

            for o in orders:
                products = self.__get_products_string(o)

                self.table.insert(
                    "",
                    tk.END,
                    values=(
                        o.id,
                        "R$%.2f" % order_price(o),
                        o.payment_method,
                        products,
                        o.created_at.strftime("%H:%M:%S"),
                    ),
                )

            self.table.pack(pady=20, padx=20)

        def __get_products_string(self, order: Order):
            result = ""
            i = 0

            while len(result) < 500 and i < len(order.products):
                product = order.products[i]
                result += "%s x %d, " % (product.product.name, product.quantity)

                i += 1

            return result[:-2]

    class Sidebar(ctk.CTkFrame):
        def __init__(self, master: "MainFrame"):
            super().__init__(master)

            self.master = master
            self.grid_rowconfigure(5, weight=1)

            self.logo_label = ctk.CTkLabel(self, text="Autostock", font=ctk.CTkFont(size=20, weight="bold"))
            self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
            self.sidebar_button_1 = ctk.CTkButton(
                self,
                text="Adicionar produto",
                command=self.show_add_form,
            )
            self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
            self.sidebar_button_2 = ctk.CTkButton(
                self,
                text="Editar produto",
                command=self.show_update_form,
            )
            self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
            self.sidebar_button_3 = ctk.CTkButton(
                self,
                text="Remover produto",
                command=self.delete_product,
                fg_color="transparent",
                border_width=1,
                text_color=("#2c2c2c", "#cecece"),
            )
            self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)

            self.sidebar_button_4 = ctk.CTkButton(
                self,
                text="Vendas do dia",
                command=self.show_orders,
            )
            self.sidebar_button_4.grid(row=4, column=0, padx=20, pady=10)

            self.appearance_mode_label = ctk.CTkLabel(self, text="Appearance Mode:", anchor="w")
            self.appearance_mode_label.grid(row=6, column=0, padx=20, pady=(10, 0))
            self.appearance_mode_optionemenu = ctk.CTkOptionMenu(
                self,
                values=["Dark", "Light"],
                command=self.change_appearance_mode_event,
            )
            self.appearance_mode_optionemenu.grid(row=7, column=0, padx=20, pady=(10, 10))

        def delete_product(self):
            selected_product = self.master.get_selected_product()
            session = DB.get_session()

            if selected_product:
                id = selected_product[0]

                confirmation = askyesno(title="Remover produto?", message="Esta ação não pode ser desfeita")

                if confirmation:
                    stmt = delete(Product).where(Product.id == id)
                    session.execute(stmt)
                    session.commit()

                    self.master.update_products()

        def show_orders(self):
            toplevel = MainFrame.OrdersWindow(self, lambda: 1)
            self.master.open_toplevel(toplevel)

        def show_add_form(self):
            toplevel = MainFrame.AddWindow(self, self.master.update_products)
            self.master.open_toplevel(toplevel)

        def show_update_form(self):
            selected_product = self.master.get_selected_product()

            if selected_product:
                toplevel = MainFrame.UpdateWindow(
                    self,
                    self.master.update_products,
                    selected_product,
                )
                self.master.open_toplevel(toplevel)

        def change_appearance_mode_event(self, new_appearance_mode: str):
            ctk.set_appearance_mode(new_appearance_mode)

        def change_scaling_event(self, new_scaling: str):
            new_scaling_float = int(new_scaling.replace("%", "")) / 100

            ctk.set_widget_scaling(new_scaling_float)

    def __init__(self, master: "App"):
        super().__init__(master)

        self.master = master

        self._selected_product = None
        self._products = []
        self.toplevel_window = None

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.sidebar = self.Sidebar(self)
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")

        self.search_frame = ctk.CTkFrame(self)
        self.search_frame.grid_columnconfigure(0, weight=1)

        self.search_input = ctk.CTkEntry(self.search_frame, placeholder_text="Buscar")
        self.search_input.grid(row=0, column=0, sticky="nsew")

        self.search_button = ctk.CTkButton(self.search_frame, text="🔍", command=self._search_product, width=64)
        self.search_button.grid(row=0, column=1, padx=(10, 0))

        self.search_frame.grid(row=0, column=1, sticky="nsew", pady=10, padx=10)

        columns = ("id", "name", "price", "ref", "qtd")

        self.table = ttk.Treeview(
            master=self,
            columns=columns,
            show="headings",
        )

        self.table.column("#1", minwidth=50, width=50)
        self.table.column("#2", minwidth=220, width=220)
        self.table.column("#3", minwidth=120, width=120)
        self.table.column("#4", minwidth=120, width=120)
        self.table.column("#5", minwidth=120, width=120)

        self.table.heading("id", anchor="w", text="ID")
        self.table.heading("name", anchor="w", text="Nome")
        self.table.heading("price", anchor="w", text="Preço")
        self.table.heading("ref", anchor="w", text="Ref.")
        self.table.heading("qtd", anchor="w", text="Quantidade")

        self.table.bind("<<TreeviewSelect>>", self._item_selected)

        self.table.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        self.update_products()

    def _search_product(self):
        self.update_products(self.search_input.get())

    def _item_selected(self, event):
        selection = self.table.selection()

        if len(selection) > 0:
            self._selected_product = self.table.item(self.table.selection()[0])["values"]

    def _show_products(self):
        self.table.delete(*self.table.get_children())

        for p in self._products:
            self.table.insert("", tk.END, values=(p.id, p.name, p.price, p.ref, p.quantity))

    def open_toplevel(self, toplevel: ctk.CTkToplevel):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = toplevel
        else:
            self.toplevel_window.focus()

    def get_selected_product(self):
        return self._selected_product

    def get_products(self):
        return self._products

    def update_products(self, filter=""):
        session = DB.get_session()
        stmt = select(Product).where(or_(Product.name.like(f"{filter}%"), Product.ref == filter))

        self._products = session.scalars(stmt)
        self._show_products()
