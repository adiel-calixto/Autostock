from enum import Enum


class PaymentMethod(Enum):
    PIX = "pix"
    CREDIT_CARD = "credit_card"
    CASH = "cash"
