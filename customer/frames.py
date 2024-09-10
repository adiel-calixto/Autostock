from tkinter import ttk
import tkinter as tk
from typing import Type, Union
import customtkinter as ctk
from sqlalchemy import select
from db import DB
from shared.enums import PaymentMethod
from shared.models import Order, OrderProduct, Product
from shared.utils import now

session = DB.get_session()


class MainFrame(ctk.CTkFrame):
    class CartFrame(ctk.CTkFrame):
        class Sidebar(ctk.CTkFrame):
            def __init__(self, parent: "MainFrame.CartFrame", order: Order):
                super().__init__(parent)

                self.__parent = parent
                self.__order = order

                self.grid_rowconfigure(1, weight=1)

                logo_label = ctk.CTkLabel(self, text="Carrinho", font=ctk.CTkFont(size=20, weight="bold"))
                logo_label.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 10))

                columns = ("name", "qtd")

                self.table = ttk.Treeview(
                    master=self,
                    columns=columns,
                    show="headings",
                )

                self.table.column("#1", width=150)
                self.table.column("#2", width=50)

                self.table.heading("name", anchor="w", text="Nome")
                self.table.heading("qtd", anchor="w", text="Qtd.")

                self.table.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=20, pady=10)

                subtotal_label = ctk.CTkLabel(self, text="SUBTOTAL: ", font=ctk.CTkFont(size=20, weight="bold"))
                subtotal_label.grid(row=2, column=0, sticky="w", padx=20)

                self.price_label = ctk.CTkLabel(self, text="R$0.00", font=ctk.CTkFont(size=20, weight="bold"))
                self.price_label.grid(row=2, column=1, sticky="e", padx=20, pady=50)

            def update(self):
                self.__list_products()
                self.__update_price()

            def __list_products(self):
                self.table.delete(*self.table.get_children())

                for p in self.__order.products:
                    self.table.insert("", tk.END, values=(p.product.name, p.quantity))

            def __update_price(self):
                total = 0

                for p in self.__order.products:
                    total += p.quantity * p.product.price

                self.price_label.configure(text="R$%.2f" % total)

        def __init__(self, master: "MainFrame", order: Order):
            super().__init__(master)

            self.__parent = master
            self.__order = order

            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(1, weight=1)

            self.sidebar = self.Sidebar(self, order)
            self.sidebar.grid(row=0, column=1, rowspan=3, sticky="nsew")

            search_frame = ctk.CTkFrame(self)
            search_frame.grid_columnconfigure(0, weight=1)

            self.search_input = ctk.CTkEntry(search_frame, placeholder_text="Buscar")
            self.search_input.grid(row=0, column=0, sticky="nsew", pady=10, padx=(10, 0))
            self.search_input.bind("<Return>", lambda _: self.__search_product())

            search_button = ctk.CTkButton(search_frame, text="+", width=64, command=self.__search_product)
            search_button.grid(row=0, column=1, pady=10, padx=10)

            search_frame.grid(row=0, column=0, sticky="nsew", pady=10, padx=10)

            self.selected_product_label = ctk.CTkLabel(
                self, text="Insira o código de um produto", font=ctk.CTkFont(size=30)
            )
            self.selected_product_label.grid(
                row=1,
                column=0,
                sticky="new",
                pady=10,
            )

            btn_frame = ctk.CTkFrame(self)

            cancel_button = ctk.CTkButton(
                btn_frame,
                text="Cancelar compra",
                height=64,
                fg_color="transparent",
                hover_color="#500000",
                border_color="#500000",
                border_width=2,
                command=self.__cancel_order,
            )
            cancel_button.grid(row=0, column=0, sticky="nse", pady=10, padx=20)

            self.finish_button = ctk.CTkButton(
                btn_frame,
                text="Pagar",
                height=64,
                fg_color="green",
                hover_color="#005000",
                command=self.__pay_order,
                state="disabled",
            )
            self.finish_button.grid(row=0, column=1, sticky="nse", pady=10, padx=20)

            btn_frame.grid(row=2, column=0, sticky="nse", pady=10, padx=20)

        def __pay_order(self):
            self.__parent._show_frame(MainFrame.PaymentFrame)

        def __cancel_order(self):
            self.__parent._reset_order()
            self.__parent._show_frame(MainFrame.StartFrame)

        def __search_product(self):
            stmt = select(Product).where(
                Product.ref == self.search_input.get(),
            )

            product = session.scalar(stmt)

            if product == None:
                self.selected_product_label.configure(text="Produto não encontrado")
                return

            self.selected_product_label.configure(text=f"%s | R$%.2f" % (product.name, product.price))
            self.__add_product(product)

        def __add_product(self, product: Product):
            existing_product_idx = -1

            for i, p in enumerate(self.__order.products):
                if p.product.id == product.id:
                    existing_product_idx = i

            if existing_product_idx != -1:
                self.__order.products[existing_product_idx].quantity += 1
            else:
                self.__order.products.append(
                    OrderProduct(
                        product=product,
                        quantity=1,
                        t_price=product.price,
                        t_ref=product.name,
                    )
                )

            self.__order_updated()

        def __order_updated(self):
            self.finish_button.configure(state="normal")
            self.sidebar.update()

    class PaymentFrame(ctk.CTkFrame):
        def __init__(self, parent: "MainFrame", order: Order):
            super().__init__(parent)

            self.__parent = parent
            self.__order = order

            label = ctk.CTkLabel(self, text="Informe o meio de pagamento", font=ctk.CTkFont(size=32))
            label.pack(pady=40)

            radio_frame = ctk.CTkFrame(self)
            self.radio_var = tk.StringVar(value="")

            for i, method in enumerate(PaymentMethod):
                radiobutton = ctk.CTkRadioButton(
                    radio_frame,
                    text=method.name,
                    variable=self.radio_var,
                    value=method.value,
                    command=self.__payment_method_selected,
                )
                radiobutton.grid(column=i, row=0, padx=10, pady=10)

            radio_frame.pack(pady=40)

            buttons_frame = ctk.CTkFrame(self)

            return_btn = ctk.CTkButton(
                buttons_frame,
                text="Voltar",
                fg_color="transparent",
                height=40,
                command=lambda: self.__parent._show_frame(MainFrame.CartFrame),
            )
            return_btn.grid(row=0, column=0, pady=10, padx=10)

            self.finish_btn = ctk.CTkButton(
                buttons_frame, text="Finalizar compra", command=self.__finish_order, state="disabled", height=40
            )
            self.finish_btn.grid(row=0, column=1, pady=10, padx=10)

            buttons_frame.pack()

        def __payment_method_selected(self):
            self.finish_btn.configure(state="normal")

        def __finish_order(self):
            self.__order.payment_method = self.radio_var.get()
            self.__order.created_at = now()
            session.commit()

            self.__parent._reset_order()
            self.__parent._show_frame(MainFrame.StartFrame)

    class StartFrame(ctk.CTkFrame):
        def __init__(self, parent: "MainFrame", order: Order):
            super().__init__(parent)

            self.__parent = parent

            label = ctk.CTkLabel(self, text="Caixa Livre")
            label.pack()

            btn = ctk.CTkButton(
                self,
                text="Iniciar compra",
                command=lambda: self.__parent._show_frame(MainFrame.CartFrame),
            )
            btn.pack()

    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frames = {}

        self._reset_order()
        self.__init_frames()

        self._show_frame(self.StartFrame)

    def __init_frames(self):
        for F in (self.StartFrame, self.CartFrame, self.PaymentFrame):
            frame = F(self, self.__current_order)
            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

    def _reset_order(self):
        session.close()

        self.__current_order = Order(user_id=1)
        self.__init_frames()

        session.add(self.__current_order)

    def _show_frame(self, cont: Type[Union[StartFrame, CartFrame, PaymentFrame]]):
        frame = self.frames[cont]
        frame.tkraise()
