from enum import Enum
from PIL import Image
import customtkinter as ctk


class PaymentMethod(Enum):
    PIX = "pix"
    CREDIT_CARD = "credit_card"
    CASH = "cash"

    def get_image(self):
        size = (64, 64)
        if self == PaymentMethod.CREDIT_CARD:
            return ctk.CTkImage(Image.open("assets/card.png"), Image.open("assets/card_i.png"), size)
        elif self == PaymentMethod.PIX:
            return ctk.CTkImage(Image.open("assets/logo_pix_i.png"), Image.open("assets/logo_pix.png"), size)
        elif self == PaymentMethod.CASH:
            return ctk.CTkImage(Image.open("assets/cash.png"), Image.open("assets/cash_i.png"), size)

    def get_name(self) -> str:
        if self == PaymentMethod.PIX:
            return "PIX"
        elif self == PaymentMethod.CREDIT_CARD:
            return "Cartão de Crédito"
        elif self == PaymentMethod.CASH:
            return "Dinheiro"
        else:
            return ""
