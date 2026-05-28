import urllib.parse


ORDER_HEADER = "Hola! Quiero hacer un pedido:\n\n"
ORDER_FOOTER = "\n\nPor favor, confirme la disponibilidad."


def format_order_line(product_name: str, quantity: int) -> str:
    return f"- {product_name} x {quantity}"


def build_order_message(lines: list[str]) -> str:
    body = "\n".join(lines)
    return f"{ORDER_HEADER}{body}{ORDER_FOOTER}"


def clean_phone_number(phone: str) -> str:
    return "".join(c for c in phone if c.isdigit())


def whatsapp_order_url(phone: str, message: str) -> str:
    digits = clean_phone_number(phone)
    encoded = urllib.parse.quote(message)
    return f"https://wa.me/{digits}?text={encoded}"
