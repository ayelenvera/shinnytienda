from django.urls import path

from . import views

app_name = "cart"

urlpatterns = [
    path("cart/", views.cart_detail, name="detail"),
    path("cart/add/<int:product_id>/", views.cart_add, name="add"),
    path("cart/remove/<int:product_id>/", views.cart_remove, name="remove"),
    path("cart/update/<int:product_id>/", views.cart_update, name="update"),
]
