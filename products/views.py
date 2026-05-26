from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET

from store.models import StoreInfo
from store.whatsapp import build_order_message, format_order_line, whatsapp_order_url

from .models import Collection, FeaturedProduct, Product, Promotion


def home(request):
    featured = (
        FeaturedProduct.objects.select_related("product")
        .filter(product__active=True)
        .order_by("priority")
    )
    collections = Collection.objects.prefetch_related("products").all()[:6]
    promotions = (
        Promotion.objects.select_related("product")
        .filter(active=True, product__active=True)
        .order_by("-discount_percentage")[:8]
    )
    return render(
        request,
        "home.html",
        {
            "featured_products": featured,
            "collections": collections,
            "promotions": promotions,
        },
    )


@require_GET
def product_list(request):
    products = Product.objects.filter(active=True).prefetch_related(
        "images", "promotions", "collections"
    )
    collections = Collection.objects.all()
    collection_slug = request.GET.get("collection")
    active_collection = None

    if collection_slug:
        active_collection = get_object_or_404(Collection, slug=collection_slug)
        products = products.filter(collections=active_collection)

    return render(
        request,
        "products/list.html",
        {
            "products": products,
            "collections": collections,
            "active_collection": active_collection,
        },
    )


@require_GET
def product_detail(request, slug):
    product = get_object_or_404(
        Product.objects.prefetch_related("images", "promotions"),
        slug=slug,
        active=True,
    )
    store = StoreInfo.load()
    message = build_order_message([format_order_line(product.name, 1)])
    whatsapp_url = whatsapp_order_url(store.whatsapp_number, message)

    return render(
        request,
        "products/detail.html",
        {
            "product": product,
            "whatsapp_url": whatsapp_url,
        },
    )
