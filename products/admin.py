from django.contrib import admin
from django.utils.html import format_html

from .models import Collection, FeaturedProduct, Product, ProductImage, Promotion


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ("image", "image_preview", "alt_text", "is_primary", "order")
    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 80px; border-radius: 4px;" />',
                obj.image.url,
            )
        return "—"

    image_preview.short_description = "Vista previa"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "code",
        "price",
        "active",
        "image_preview",
        "created_at",
    )
    list_filter = ("active", "created_at")
    search_fields = ("name", "code", "description")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("created_at", "image_preview_large")
    inlines = [ProductImageInline]
    fieldsets = (
        (None, {"fields": ("name", "slug", "code", "description")}),
        ("Precio y estado", {"fields": ("price", "active", "created_at")}),
        ("Vista previa", {"fields": ("image_preview_large",)}),
    )

    def image_preview(self, obj):
        img = obj.primary_image
        if img and img.image:
            return format_html(
                '<img src="{}" style="max-height: 40px; border-radius: 4px;" />',
                img.image.url,
            )
        return "—"

    image_preview.short_description = "Imagen"

    def image_preview_large(self, obj):
        img = obj.primary_image
        if img and img.image:
            return format_html(
                '<img src="{}" style="max-height: 200px; border-radius: 8px;" />',
                img.image.url,
            )
        return "Sin imágenes"

    image_preview_large.short_description = "Imagen principal"


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ("name", "image_preview")
    prepopulated_fields = {"slug": ("name",)}

    fields = (
        "name",
        "slug",
        "banner_text",
        "description",
        "image",
        "mobile_image",
        "image_preview",
        "products",
    )

    filter_horizontal = ("products",)

    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 120px; border-radius: 8px;" />',
                obj.image.url
            )
        return "Sin imagen"

    image_preview.short_description = "Vista previa"


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ("product", "discount_percentage", "active")
    list_filter = ("active",)
    search_fields = ("product__name", "product__code")
    autocomplete_fields = ("product",)


@admin.register(FeaturedProduct)
class FeaturedProductAdmin(admin.ModelAdmin):
    list_display = ("product", "priority", "image_preview")
    ordering = ("priority",)
    autocomplete_fields = ("product",)

    def image_preview(self, obj):
        img = obj.product.primary_image
        if img and img.image:
            return format_html(
                '<img src="{}" style="max-height: 40px; border-radius: 4px;" />',
                img.image.url,
            )
        return "—"

    image_preview.short_description = "Imagen"
