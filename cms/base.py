from django.db import models


# creating the base model for the cms.
class BaseModelCms(models.Model):
    created_by = models.CharField(
        max_length=20,
        null=True,
        blank=True,
    )
    updated_by = models.CharField(
        max_length=20,
        null=True,
        blank=True,
    )
