from datetime import datetime, timedelta, timezone
import importlib
from PIL import Image
import customtkinter as ctk
from sqlalchemy import select
from sqlalchemy.sql import func

from auth.models import User
from db import DB

MODELS_TO_LOAD = [
    "auth",
    "shared",
]


def import_models():
    for pkg in MODELS_TO_LOAD:
        importlib.import_module(f"{pkg}.models")


def now():
    return datetime.now().astimezone(timezone(timedelta(hours=-3)))


def get_logo_image():
    return ctk.CTkImage(
        dark_image=Image.open("assets/logo_horizontal_i.png"),
        light_image=Image.open("assets/logo_horizontal.png"),
        size=(180, 101),
    )


def create_default_users():
    session = DB.get_session()
    query = select(func.count(User.id))

    users_count = session.execute(query).scalar()

    if users_count and users_count > 0:
        return

    for [username, is_admin] in [("admin", True), ("caixa", False)]:
        user = User(name=username, password=username, is_admin=is_admin)
        session.add(user)

    session.commit()
