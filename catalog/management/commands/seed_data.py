# catalog/management/commands/seed_data.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from catalog.models import ProductCategory, Product, ProductImage
from decimal import Decimal
import random

User = get_user_model()

class Command(BaseCommand):
    help = "Seed the database with sample product categories, products, and images (currency: XAF)."

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Seeding database..."))

        # Ensure at least one user exists (as creator)
        admin_user, _ = User.objects.get_or_create(
            username="admin",
            defaults={
                "email": "admin@example.com",
                "is_staff": True,
                "is_superuser": True,
            },
        )
        admin_user.set_password("admin123")
        admin_user.save()

        # Sample categories
        categories_data = [
            {"name": "Electronics", "slug": "electronics"},
            {"name": "Books", "slug": "books"},
            {"name": "Clothing", "slug": "clothing"},
        ]

        categories = []
        for cat in categories_data:
            category, _ = ProductCategory.objects.get_or_create(
                name=cat["name"],
                slug=cat["slug"],
                defaults={
                    "is_active": True,
                    "created_by": admin_user,
                    "updated_by": admin_user,
                },
            )
            categories.append(category)

        # Sample products per category
        for category in categories:
            for i in range(1, 6):
                product, _ = Product.objects.get_or_create(
                    sku=f"{category.slug.upper()}-{i}",
                    slug=f"{category.slug}-{i}",
                    defaults={
                        "title": f"Sample {category.name} {i}",
                        "description": f"This is a description for {category.name} {i}.",
                        "price": Decimal(random.randint(5000, 150000)),  # realistic XAF range
                        "currency": "XAF",
                        "is_active": True,
                        "product_category": category,
                        "created_by": admin_user,
                        "updated_by": admin_user,
                    },
                )

                # Add product images
                for j in range(1, 3):
                    ProductImage.objects.get_or_create(
                        product=product,
                        url=f"https://via.placeholder.com/600x400.png?text={category.name}+{i}+Image+{j}",
                        defaults={
                            "alt": f"{category.name} {i} Image {j}"
                        },
                    )

        self.stdout.write(self.style.SUCCESS("Database seeding completed successfully!"))
