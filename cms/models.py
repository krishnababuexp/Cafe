from django.db import models
from cms.base import BaseModelCms
from cafe.validation import istelephonevalidator, iscontactvalidator


# model for the cafe cms.
class CafeCms(BaseModelCms):
    name = models.CharField(
        max_length=255,
        null=False,
        blank=False,
    )
    photo = models.ImageField(
        upload_to="cafe_cms_image",
        null=False,
        blank=False,
    )
    cafe_email = models.EmailField(
        verbose_name="E-mail",
        max_length=255,
        unique=True,
        null=True,
        blank=True,
    )
    email_1 = models.EmailField(
        verbose_name="E-mail",
        max_length=255,
        unique=True,
        null=True,
        blank=True,
    )
    email_2 = models.EmailField(
        verbose_name="E-mail",
        max_length=255,
        unique=True,
        null=True,
        blank=True,
    )
    mobile_no1 = models.CharField(
        max_length=10,
        validators=[iscontactvalidator],
        blank=True,
        null=True,
    )
    mobile_no2 = models.CharField(
        max_length=10,
        validators=[iscontactvalidator],
        blank=True,
        null=True,
    )
    mobile_no3 = models.CharField(
        max_length=10,
        validators=[iscontactvalidator],
        blank=True,
        null=True,
    )
    telephone = models.CharField(
        max_length=10,
        validators=[istelephonevalidator],
        blank=True,
        null=True,
    )
    location = models.CharField(
        max_length=255,
        blank=False,
        null=False,
    )
    pana_number = models.PositiveBigIntegerField(
        null=True,
        blank=True,
    )
    # additional information.
    discount_rate = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True,
    )
    additional_amount = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )

    def __str__(self):
        return self.name
