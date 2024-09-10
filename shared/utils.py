from datetime import datetime, timedelta, timezone
import importlib

MODELS_TO_LOAD = [
    "auth",
    "shared",
]


def import_models():
    for pkg in MODELS_TO_LOAD:
        importlib.import_module(f"{pkg}.models")


def now():
    return datetime.now().astimezone(timezone(timedelta(hours=-3)))
