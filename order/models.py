from django.db import models
from stock.models import Table, Stock, Product
from account.models import User
import uuid


# model for the order.
class Order(models.Model):
    order_number = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        unique=True,
    )
    order_date = models.DateField(
        auto_now_add=True,
        blank=True,
        null=True,
    )
    order_time = models.TimeField(
        auto_now_add=True,
        blank=True,
        null=True,
    )
    order_taken_by = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )
    tabel_number = models.ForeignKey(
        Table,
        on_delete=models.DO_NOTHING,
        blank=False,
        null=False,
    )
    total_price = models.PositiveBigIntegerField(
        blank=True,
        null=True,
    )

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self.generate_order_number()
        super().save(*args, **kwargs)

    def generate_order_number(self):
        return str(uuid.uuid4().hex[:4]).upper()

    def calculate_total_price(self):
        total = sum(
            item.product.user_price * item.quantity for item in self.order_item.all()
        )
        self.total_price = total
        self.save()

    def __str__(self):
        return f"{self.order_number}"


# model to store the order items.
class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name="order_item",
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveBigIntegerField(
        blank=True,
        null=True,
    )
    product = models.ForeignKey(
        Stock,
        on_delete=models.CASCADE,
        related_name="stock",
        blank=False,
        null=False,
    )

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
