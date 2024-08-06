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
