from django.db import models


class StoreInfo(models.Model):
    store_name = models.CharField(max_length=200, default="Shinny Tienda")
    logo = models.ImageField(upload_to="store/", blank=True, null=True)

    whatsapp_number = models.CharField(
        max_length=20,
        help_text="Número con código de país, ej: 595981123456",
    )

    instagram_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)
    tiktok_url = models.URLField(blank=True)
    location = models.TextField(blank=True, verbose_name="Dirección")
    email = models.EmailField(blank=True)

    class Meta:
        verbose_name = "Información de la tienda"
        verbose_name_plural = "Información de la tienda"

    def __str__(self):
        return self.store_name

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj