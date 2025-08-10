from django.conf import settings
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models

sku_validator = RegexValidator(r"^[A-Z0-9\-_.]+$", "SKU must be A-Z, 0-9, -, _, .")

class ProductCategory(models.Model):
    name = models.CharField(max_length=120, unique=True, db_index=True)
    slug = models.SlugField(max_length=140, unique=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="product_categories_created")
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name="product_categories_updated", null=True, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self): return self.name


class Product(models.Model):
    sku = models.CharField(max_length=40, unique=True, validators=[sku_validator])
    title = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=220, unique=True)
    product_category = models.ForeignKey(ProductCategory, on_delete=models.PROTECT, related_name="products")
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], db_index=True)
    currency = models.CharField(max_length=3, default="USD")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="products_created")
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name="products_updated", null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["product_category", "price"]),
            models.Index(fields=["is_active", "product_category", "price"]),
            models.Index(fields=["slug"]),
        ]

    def __str__(self): return self.title


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    url = models.URLField()
    alt = models.CharField(max_length=160, blank=True)

    def __str__(self): return f"Image<{self.product_id}>"
