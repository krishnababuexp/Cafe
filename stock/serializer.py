from rest_framework import serializers
from .models import Catogery, Supplier, Stock


# Serializer for the Catogery.
class Catogery_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Catogery
        fields = "__all__"


# Serializer for the Suppliers.
class Suppliers_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = "__all__"


# Serializer for the stock create.
class StockCreate_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = "__all__"

    def validate(self, attrs):
        product_name = attrs.get("name")
        product_price = attrs.get("price")
        product_quantity = attrs.get("quantity")
        # here we have to check if the product is already exists or not.
        stock_data = Stock.objects.all()
        for stock in stock_data:
            if product_name == stock.name:
                # here we have to extract the id of the product.
                product_id = Stock.objects.get(name=product_name)
                raise serializers.ValidationError(
                    {
                        "msg": f"Product '{product_id.name}' already exists with ID '{product_id.id}'"
                    }
                )
            elif product_price == 0:
                raise serializers.ValidationError(
                    {"msg": "The price is set to 0. Proceed?"}
                )
        return attrs


# catogery list for the stock including certain data.
class CatogeryStock_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Catogery
        fields = ("id", "name")


# suppilier list for the stock including certain data.
class SuppliersStock_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ("id", "name")


# Serializer for the stock for the admin.
class StockAdmin_Serializer(serializers.ModelSerializer):
    catogery = CatogeryStock_Serializer()
    supplier = SuppliersStock_Serializer()

    class Meta:
        model = Stock
        fields = "__all__"


# Serializer for the stock for the user.
class StockUser_Serializer(serializers.ModelSerializer):
    catogery = CatogeryStock_Serializer()

    class Meta:
        model = Stock
        exclude = ["created_at", "updated_at", "supplier", "product_code"]


# Serializer for the stock.
class Stock_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = "__all__"


# Serializer for the total price.
class StockTotalPrice_Serializer(serializers.ModelSerializer):
    stock_total_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    class Meta:
        model = Stock
        exclude = [
            "name",
            "photo",
            "product_code",
            "description",
            "catogery",
            "supplier",
            "home_price",
            "user_price",
            "quantity",
            "total_price",
            "id",
            "created_at",
            "updated_at",
        ]
