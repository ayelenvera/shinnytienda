from cart.session_cart import SessionCart

from .models import StoreInfo


def store_context(request):
    store = StoreInfo.load()
    cart = SessionCart(request)
    return {
        "store_info": store,
        "cart_item_count": cart.item_count,
    }
