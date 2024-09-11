from .models import Order, Stock, OrderItem, Product, Table, User
from rest_framework import serializers, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.db import transaction


# Serializer for the table detial.
class TableDetail_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        exclude = ("available", "created_at", "updated_at")


# Serializer for the user detail.
class UserDetail_Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = (
            "photo",
            "first_name",
            "last_name",
            "date_created",
            "date_updated",
            "is_admin",
            "is_active",
            "is_superuser",
            "password",
            "last_login",
        )


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
            "table_number",
            "total_price",
            "order_item",
        ]
        read_only_fields = [
            "order_number",
            "order_date",
            "order_time",
            "total_price",
        ]

    def validate_stock(self, product, quantity):
        try:
            stock = get_object_or_404(Stock, product=product)
            if stock.remaining_quantity < quantity:
                raise serializers.ValidationError(
                    {"msg": f"We don't have {quantity} of {product.name}"}
                )
            return stock
        except Http404:
            return None

    def create(self, validated_data):
        with transaction.atomic():
            order_item_data = validated_data.pop("order_item")
            table_no = validated_data["table_number"]

            # Check and update stock for each item
            for item_data in order_item_data:
                product = item_data["product"]
                quantity = item_data["quantity"]
                stock = self.validate_stock(product, quantity)

            # Create the order and order items
            order = Order.objects.create(**validated_data)
            for item_data in order_item_data:
                product = item_data["product"]
                quantity = item_data["quantity"]
                stock = self.validate_stock(product, quantity)

                OrderItem.objects.create(order=order, **item_data)

                if stock:
                    rqtn = stock.remaining_quantity - quantity
                    stock.remaining_quantity -= quantity
                    stock.remaining_quantity_total_price = rqtn * stock.home_price
                    stock.save()

            order.calculate_total_price()

            # Update table availability
            table_data = get_object_or_404(Table, table_number=table_no.table_number)
            table_data.available = False
            table_data.save()

            return order


# Serializer for the order list according to the table.
class TableOrderList_Serializer(serializers.ModelSerializer):
    product_id = serializers.SerializerMethodField()
    product = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    order_product_price = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product_id",
            "product",
            "quantity",
            "price",
            "order_product_price",
        ]

    def get_product(self, obj):
        return obj.product.name

    def get_price(self, obj):
        return obj.product.user_price

    def get_order_product_price(self, obj):
        pd = obj.product.user_price
        qtn = obj.quantity
        return pd * qtn

    def get_product_id(self, obj):
        return obj.product.id


# serializer for the order retrival.
class OrderListAdmin_Serializer(serializers.ModelSerializer):
    order_item = TableOrderList_Serializer(many=True)
    table_number = TableDetail_Serializer()
    order_taken_by = UserDetail_Serializer()

    class Meta:
        model = Order
        fields = "__all__"


# Serializer for the order / order item update.
class OrderItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["product", "quantity"]

    def validate(self, data):
        product = data.get("product")
        quantity = data.get("quantity")
        print(product)
        print(quantity)

        # Validate stock
        try:
            stock = Stock.objects.get(product=product)
        except Stock.DoesNotExist:
            stock = None
        print(stock)
        if stock is not None:
            if stock.remaining_quantity < quantity:
                raise serializers.ValidationError(
                    {
                        "msg": f"We don't have {quantity} units of {product.name} in stock."
                    }
                )
        return data


# Serializer to update the order.
class OrderUpdateSerializer(serializers.ModelSerializer):
    order_item = OrderItemUpdateSerializer(many=True)

    class Meta:
        model = Order
        fields = ["order_item", "table_number", "order_taken_by"]

    def update(self, instance, validated_data):
        order_items_data = validated_data.pop("order_item")

        # Update table_number and order_taken_by if provided
        instance.table_number = validated_data.get(
            "table_number", instance.table_number
        )
        instance.order_taken_by = validated_data.get(
            "order_taken_by", instance.order_taken_by
        )
        instance.save()
        with transaction.atomic():
            for item_data in order_items_data:
                product = item_data.get("product")
                new_quantity = item_data.get("quantity")

                # Get the existing OrderItem instance or create a new one
                order_item, created = OrderItem.objects.get_or_create(
                    order=instance, product=product, defaults={"quantity": new_quantity}
                )

                # Handle the stock update if the item already existed
                if not created:
                    existing_quantity = order_item.quantity
                    quantity_difference = new_quantity - existing_quantity
                    try:
                        stock = Stock.objects.get(product=product)
                    except Stock.DoesNotExist:
                        stock = None

                    if stock is not None:
                        if quantity_difference > 0:  # Quantity increased
                            if stock.remaining_quantity < quantity_difference:
                                raise serializers.ValidationError(
                                    {
                                        "msg": f"Not enough stock for {product.name}. Available: {stock.remaining_quantity}, requested: {quantity_difference} more."
                                    }
                                )
                            stock.remaining_quantity -= quantity_difference
                            rqtn = stock.remaining_quantity - quantity_difference
                            stock.remaining_quantity_total_price = (
                                rqtn * stock.home_price
                            )
                            stock.save()
                        else:  # Quantity decreased
                            stock.remaining_quantity += abs(quantity_difference)
                            rqtn = stock.remaining_quantity + quantity_difference
                            stock.remaining_quantity_total_price = (
                                rqtn * stock.home_price
                            )
                            stock.save()

                    # Update the existing OrderItem quantity
                    order_item.quantity = new_quantity
                    order_item.save()

                else:
                    try:
                        stock = Stock.objects.get(product=product)
                    except Stock.DoesNotExist:
                        stock = None
                    if stock is not None:
                        if stock.remaining_quantity < new_quantity:
                            raise serializers.ValidationError(
                                {
                                    "msg": f"Not enough stock for {product.name}. Available: {stock.quantity}, requested: {new_quantity}."
                                }
                            )
                        stock.remaining_quantity -= new_quantity
                        rqtn = stock.remaining_quantity - new_quantity
                        stock.remaining_quantity_total_price = rqtn * stock.home_price
                        stock.save()

            # Recalculate the total price of the order
            instance.calculate_total_price()

        return instance
