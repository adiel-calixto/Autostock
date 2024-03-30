from typing import List
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, relationship
from sqlalchemy.orm import mapped_column

from shared.models import Order, Product


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    password: Mapped[str] = mapped_column(String(40))
    is_admin: Mapped[bool] = mapped_column(default=False)
    products: Mapped[List[Product]] = relationship()
    orders: Mapped[List[Order]] = relationship()

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, is_admin={self.is_admin!r})"
