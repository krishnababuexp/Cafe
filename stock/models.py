from django.db import models
from .base import BaseModel
from cafe.validation import isalphanumericalvalidator


# model for the product catogery.
class Catogery(BaseModel):
    name = models.CharField(
        max_length=100,
        blank=False,
        null=False,
    )
    photo = models.FileField(
        upload_to="Product-Catogery",
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name


# model for the suppilers.
class Supplier(BaseModel):
    name = models.CharField(
        max_length=250,
        blank=False,
        null=False,
    )
    phone_number = models.PositiveBigIntegerField(
        blank=False,
        null=False,
    )

    def __str__(self):
        return self.name


# model for the stock.
class Product(BaseModel):
    # product details.
    name = models.CharField(
        max_length=250,
        blank=False,
        null=False,
        validators=[isalphanumericalvalidator],
    )
    photo = models.FileField(
        upload_to="product_image",
        null=True,
        blank=True,
    )
    product_code = models.PositiveIntegerField(
        blank=True,
        null=True,
        unique=True,
        default=000,
    )
    description = models.TextField(
        blank=True,
        null=True,
    )
    catogery = models.ForeignKey(
        Catogery,
        on_delete=models.CASCADE,
        related_name="product",
    )
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.CASCADE,
        related_name="products",
        blank=True,
        null=True,
    )
    user_price = models.PositiveBigIntegerField(
        blank=False,
        null=False,
    )

    def __str__(self):
        return f"{self.name}-{self.product_code}-{self.user_price}"


# creating the model for the stock.
class Stock(BaseModel):
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        related_name="stock_product",
        blank=False,
        null=False,
    )
    home_price = models.PositiveBigIntegerField(
        blank=False,
        null=False,
    )
    quantity = models.PositiveBigIntegerField(
        null=False,
        blank=False,
    )
    total_price = models.PositiveBigIntegerField(
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.product.name}-{self.quantity}-{self.home_price}"


# model for the table.
class Table(BaseModel):
    table_number = models.IntegerField(
        null=False,
        blank=False,
        primary_key=True,
    )
    table_name = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        unique=True,
    )
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.table_name}-{self.table_number}"
