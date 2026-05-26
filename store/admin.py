from django.contrib import admin
from django.utils.html import format_html

from .models import StoreInfo


@admin.register(StoreInfo)
class StoreInfoAdmin(admin.ModelAdmin):
    list_display = (
        "store_name",
        "whatsapp_number",
        "instagram_url",
        "facebook_url",
        "tiktok_url",
        "location",
        "email",
    )
    fieldsets = (
        ("Tienda", {"fields": ("store_name", "logo", "logo_preview")}),
        (
            "Contacto y redes sociales",
            {
                "fields": (
                    "whatsapp_number",
                    "instagram_url",
                    "facebook_url",
                    "tiktok_url",
                    "location",
                    "email",
                )
            },
        ),
    )
    readonly_fields = ("logo_preview",)

    def logo_preview(self, obj):
        if obj.logo:
            return format_html(
                '<img src="{}" style="max-height: 120px; border-radius: 8px;" />',
                obj.logo.url,
            )
        return "Sin logo"

    logo_preview.short_description = "Vista previa del logo"

    def has_add_permission(self, request):
        return not StoreInfo.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
