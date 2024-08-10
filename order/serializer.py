from .models import Order, Stock, OrderItem
from rest_framework import serializers, permissions, status
from rest_framework.response import Response


# Serializer for the order list.
class OrderList_Serializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["product", "quantity"]


# Serializer for the order.
class OrderCreate_Serializer(serializers.ModelSerializer):
    order_item = OrderList_Serializer(many=True)

    class Meta:
        model = Order
        fields = [
            "order_number",
            "order_date",
            "order_time",
            "order_taken_by",
            "tabel_number",
            "total_price",
            "order_item",
        ]
        read_only_fields = [
            "order_number",
            "order_date",
            "order_time",
            "total_price",
        ]

    def create(self, validated_data):
        order_item_data = validated_data.pop("order_item")
        print(order_item_data)
        order = Order.objects.create(**validated_data)

        for item_data in order_item_data:
            # extracting the data form the request.
            product = item_data["product"]
            quantity = item_data["quantity"]
            stock_data = Stock.objects.get(id=product.id)
            if stock_data.quantity < quantity:
                raise serializers.ValidationError(
                    {"msg": f"We dont have {quantity} of {product}!!"},
                )
            stock_data.quantity -= quantity
            OrderItem.objects.create(order=order, **item_data)
            stock_data.save()

        order.calculate_total_price()
        return order
