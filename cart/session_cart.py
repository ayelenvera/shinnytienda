from decimal import Decimal

from products.models import Product


SESSION_KEY = "shinny_cart"


class SessionCart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(SESSION_KEY)
        if cart is None:
            cart = self.session[SESSION_KEY] = {}
        self.cart = cart

    def add(self, product_id: int, quantity: int = 1):
        product_id = str(product_id)
        self.cart[product_id] = self.cart.get(product_id, 0) + quantity
        self.save()

    def remove(self, product_id: int):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def set_quantity(self, product_id: int, quantity: int):
        product_id = str(product_id)
        if quantity <= 0:
            self.remove(product_id)
        else:
            self.cart[product_id] = quantity
            self.save()

    def clear(self):
        self.session[SESSION_KEY] = {}
        self.cart = self.session[SESSION_KEY]
        self.save()

    def save(self):
        self.session.modified = True

    def __iter__(self):
        product_ids = [int(pid) for pid in self.cart.keys()]
        products = Product.objects.filter(pk__in=product_ids, active=True)
        product_map = {p.pk: p for p in products}

        for product_id, quantity in self.cart.items():
            product = product_map.get(int(product_id))
            if product:
                yield {
                    "product": product,
                    "quantity": quantity,
                    "line_total": product.discounted_price() * quantity,
                }

    def __len__(self):
        return sum(self.cart.values())

    @property
    def item_count(self):
        return sum(self.cart.values())

    @property
    def subtotal(self) -> Decimal:
        total = Decimal("0.00")
        for item in self:
            total += item["line_total"]
        return total

    def order_lines(self) -> list[str]:
        from store.whatsapp import format_order_line

        return [
            format_order_line(item["product"].name, item["quantity"])
            for item in self
        ]
