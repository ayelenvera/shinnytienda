from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from products.models import Product
from store.models import StoreInfo
from store.whatsapp import build_order_message, whatsapp_order_url

from .session_cart import SessionCart


def cart_detail(request):
    cart = SessionCart(request)
    store = StoreInfo.load()
    whatsapp_url = None

    if cart.item_count > 0:
        message = build_order_message(cart.order_lines())
        whatsapp_url = whatsapp_order_url(store.whatsapp_number, message)

    return render(
        request,
        "cart/detail.html",
        {
            "cart": cart,
            "whatsapp_url": whatsapp_url,
        },
    )


@require_POST
def cart_add(request, product_id):
    product = get_object_or_404(Product, pk=product_id, active=True)
    cart = SessionCart(request)
    quantity = int(request.POST.get("quantity", 1))
    cart.add(product.pk, max(1, quantity))
    messages.success(request, f"«{product.name}» agregado al carrito.")
    next_url = request.POST.get("next", product.get_absolute_url())
    return redirect(next_url)


@require_POST
def cart_remove(request, product_id):
    cart = SessionCart(request)
    cart.remove(product_id)
    messages.info(request, "Producto eliminado del carrito.")
    return redirect("cart:detail")


@require_POST
def cart_update(request, product_id):
    cart = SessionCart(request)
    quantity = int(request.POST.get("quantity", 1))
    cart.set_quantity(product_id, quantity)
    return redirect("cart:detail")
