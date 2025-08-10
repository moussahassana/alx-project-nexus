from rest_framework import serializers
from .models import ProductCategory, Product, ProductImage

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "url", "alt"]

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ["id", "name", "slug", "is_active"]

class ProductSerializer(serializers.ModelSerializer):
    product_category = ProductCategorySerializer(read_only=True)
    product_category_id = serializers.PrimaryKeyRelatedField(
        queryset=ProductCategory.objects.all(), source="product_category", write_only=True
    )
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id","sku","title","slug","description","price","currency","is_active",
            "product_category","product_category_id","images","created_at","updated_at"
        ]
