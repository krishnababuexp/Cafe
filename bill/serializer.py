from rest_framework import serializers
from .models import Bill
from order.serializer import OrderListAdmin_Serializer
from cms.serializers import CmsSerializer
from cms.models import CafeCms
from order.models import Order, OrderItem
from stock.serializer import TablePartial_Serializer


# Serilaizer for the bill create.
class BillCreate_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = "__all__"


# Serializer for the order list according to the table.
class TableOrderList_Serializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()
    serial_number = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ["serial_number", "product", "quantity", "price", "total_price"]

    def get_product(self, obj):
        return obj.product.name

    def get_price(self, obj):
        product = obj.product
        return product.user_price

    def get_total_price(self, obj):
        product = obj.product.user_price
        return obj.quantity * product

    def get_serial_number(self, obj):
        index = self.context.get("serial_num", 1)
        self.context["serial_num"] = index + 1
        return index


# Serailzer for the order list for the bill print data.
class BillOrderDetail_Serializer(serializers.ModelSerializer):
    order_list = serializers.SerializerMethodField()
    table_number = TablePartial_Serializer()

    class Meta:
        model = Order
        fields = (
            "order_number",
            "order_list",
            "total_price",
            "table_number",
        )

    def get_order_list(self, obj):
        order_list = obj.order_item.all()
        print(order_list)
        return TableOrderList_Serializer(order_list, many=True).data


# Serializer for the bill list for the admin.
class BillList_Serializer(serializers.ModelSerializer):
    order = BillOrderDetail_Serializer()

    class Meta:
        model = Bill
        fields = "__all__"


# Serializer for the bill data.
class BillDetail_Serializer(serializers.ModelSerializer):
    cafe = serializers.SerializerMethodField()
    order = BillOrderDetail_Serializer()

    class Meta:
        model = Bill
        fields = (
            "cafe",
            "bill_number",
            "bill_created",
            "bill_time",
            "order",
            "discount_amount",
            "grand_total",
        )

    def get_cafe(self, obj):
        cafe_data = CafeCms.objects.first()
        if cafe_data:
            return {
                "name": cafe_data.name,
                "photo": cafe_data.photo.url if cafe_data.photo else None,
                "email": cafe_data.cafe_email,
                "mobile_contact": cafe_data.mobile_no1,
                "telephone": cafe_data.telephone,
                "address": cafe_data.location,
                "additional_amount": cafe_data.additional_amount,
                "pan_number": cafe_data.pan_number,
            }
