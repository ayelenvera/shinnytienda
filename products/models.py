from decimal import Decimal

from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField()
    code = models.CharField(max_length=50, unique=True, verbose_name="SKU")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name) or "producto"
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("products:detail", kwargs={"slug": self.slug})

    @property
    def primary_image(self):
        image = self.images.filter(is_primary=True).first()
        if image:
            return image
        return self.images.first()

    def get_active_promotion(self):
        return self.promotions.filter(active=True).first()

    def discounted_price(self):
        promotion = self.get_active_promotion()
        if promotion:
            discount = self.price * Decimal(promotion.discount_percentage) / Decimal(100)
            return self.price - discount
        return self.price


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="products/%Y/%m/")
    alt_text = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Imagen de producto"
        verbose_name_plural = "Imágenes de producto"

    def __str__(self):
        return f"{self.product.name} — imagen {self.pk}"


class Collection(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="collections/", blank=True, null=True)
    mobile_image = models.ImageField(
        upload_to="collections/mobile/",
        blank=True,
        null=True,
        verbose_name="Imagen móvil",
    )
    banner_text = models.CharField(max_length=255, blank=True)

    products = models.ManyToManyField(
        Product,
        related_name="collections",
        blank=True
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Colección"
        verbose_name_plural = "Colecciones"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name) or "coleccion"
            slug = base_slug
            counter = 1
            while Collection.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("products:list") + f"?collection={self.slug}"


class Promotion(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="promotions"
    )
    discount_percentage = models.PositiveIntegerField()
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Promoción"
        verbose_name_plural = "Promociones"

    def __str__(self):
        return f"{self.product.name} — {self.discount_percentage}% off"


class FeaturedProduct(models.Model):
    product = models.OneToOneField(
        Product, on_delete=models.CASCADE, related_name="featured"
    )
    priority = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["priority", "id"]
        verbose_name = "Producto destacado"
        verbose_name_plural = "Productos destacados"

    def __str__(self):
        return self.product.name
