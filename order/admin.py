from django.contrib import admin
from .models import Order, OrderItem


# admin pannel for the order.
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "order_number",
        "order_date",
        "order_time",
        "order_taken_by",
        "table_number",
        "total_price",
        # "order_item",
    ]


admin.site.register(Order, OrderAdmin)


# admin pannel for the OrderList.
class OrderList_Admin(admin.ModelAdmin):
    list_display = ["id", "order", "quantity", "product"]


admin.site.register(OrderItem, OrderList_Admin)
