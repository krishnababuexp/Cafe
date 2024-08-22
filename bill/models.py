from django.db import models
from order.models import Order


# model for the billig.
class Bill(models.Model):
    bill_number = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    order = models.OneToOneField(
        Order,
        on_delete=models.DO_NOTHING,
        blank=False,
        null=False,
    )
    discount_amount = models.PositiveBigIntegerField(
        blank=True,
        null=True,
    )
    discount_rate = models.PositiveBigIntegerField(
        blank=True,
        null=True,
    )
    grand_total = models.PositiveBigIntegerField(
        blank=True,
        null=True,
    )
    bill_created = models.DateField(
        auto_now_add=True,
    )
    bill_time = models.TimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return f"{self.bill_number}_{self.order.order_number}"
