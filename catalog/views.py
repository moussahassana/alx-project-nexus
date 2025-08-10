# catalog/views.py
from django.db.models import Prefetch
from rest_framework import viewsets, permissions
from .models import ProductCategory, Product, ProductImage
from .serializers import ProductCategorySerializer, ProductSerializer
from .filters import ProductFilter


class ProductCategoryViewSet(viewsets.ModelViewSet):
    """
    CRUD for product categories.
    - List: fetch only lightweight columns.
    - Retrieve/Write: full object (still small).
    """
    serializer_class = ProductCategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = "slug"
    filterset_fields = ["is_active"]
    search_fields = ["name"]
    ordering_fields = ["name"]

    def get_queryset(self):
        qs = ProductCategory.objects.all()
        if self.action == "list":
            # Lighter payload for collections
            return qs.only("id", "name", "slug", "is_active")
        return qs

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class ProductViewSet(viewsets.ModelViewSet):
    """
    CRUD for products with filtering/sorting/pagination.
    - List: select_related category, prefetch images, and return only common fields.
    - Retrieve: full record (includes description), with related objects.
    """
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = "slug"
    filterset_class = ProductFilter
    search_fields = ["title", "sku", "description"]
    ordering_fields = ["price", "created_at", "title"]
    ordering = ["-created_at"]

    def get_queryset(self):
        # Shared related optimizations
        base = (
            Product.objects
            .select_related("product_category")
            .prefetch_related(
                Prefetch(
                    "images",
                    queryset=ProductImage.objects.only("id", "url", "alt", "product_id")
                )
            )
        )

        if self.action == "list":
            # Keep the list view fast: avoid large text fields and unused columns
            return base.only(
                "id", "sku", "title", "slug",
                "price", "currency", "is_active",
                "product_category_id",
                "created_at", "updated_at",
                # from select_related target
                "product_category__id", "product_category__name", "product_category__slug", "product_category__is_active",
            )
        # For retrieve/create/update/destroy: return full object (description included)
        return base

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)
