from django.contrib import admin
from bill.models import Bill

# Register your models here.


class Bill_Admin(admin.ModelAdmin):
    list_display = (
        "id",
        "bill_number",
        "order",
        "discount_amount",
        "discount_rate",
        "grand_total",
    )


admin.site.register(Bill, Bill_Admin)
