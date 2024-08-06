from django.db import models
from .base import BaseModel


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
