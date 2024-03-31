from datetime import datetime
from typing import List, Optional
from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import BaseModel


class Product(BaseModel):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    ref: Mapped[str] = mapped_column(String(10))
    price: Mapped[float] = mapped_column()
    orders: Mapped[List["OrderProduct"]] = relationship(back_populates="product")
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )


class OrderProduct(BaseModel):
    __tablename__ = "order_product"
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), primary_key=True)
    t_price: Mapped[float] = mapped_column()
    t_ref: Mapped[Optional[str]] = mapped_column(String(10))
    quantity: Mapped[int] = mapped_column()
    product: Mapped["Product"] = relationship(back_populates="orders")
    order: Mapped["Order"] = relationship(back_populates="products")


class Order(BaseModel):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    products: Mapped[List["OrderProduct"]] = relationship(back_populates="order")
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )
