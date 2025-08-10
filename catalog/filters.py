import django_filters as df
from .models import Product

class ProductFilter(df.FilterSet):
    product_category = df.NumberFilter(field_name="product_category_id", lookup_expr="exact")
    min_price = df.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = df.NumberFilter(field_name="price", lookup_expr="lte")
    is_active = df.BooleanFilter()

    class Meta:
        model = Product
        fields = ["product_category", "is_active"]
