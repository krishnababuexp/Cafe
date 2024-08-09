from django.contrib import admin
from .models import Catogery, Supplier, Stock, Table

# Register your models here.
admin.site.register(Catogery)
admin.site.register(Supplier)
admin.site.register(Stock)


class TableAdmin(admin.ModelAdmin):
    list_display = (
        "table_number",
        "table_name",
        "available",
    )


admin.site.register(Table, TableAdmin)
