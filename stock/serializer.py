from rest_framework import serializers
from .models import Catogery, Supplier, Product, Table, Stock


# Serializer for the Catogery.
class Catogery_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Catogery
        fields = "__all__"


# Serializer for the catogery image validation.
class CatogeryCreate_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Catogery
        fields = "__all__"

    def validate_photo(self, value):
        valid_extnsion = ["png", "jpg", "jpeg", "hiec"]
        extension = value.name.split(".")[-1].lower()
        print(value.name)
        data = self.initial_data.get("name")
        print(data)
        if extension not in valid_extnsion:
            raise serializers.ValidationError(
                f"Unsupported file extension: {extension}.Use [jpg,jpeg,png,hiec]"
            )
        else:
            new_name = f"{data}.{extension}"
            value.name = new_name
        return value


# Serializer for the Suppliers.
class Suppliers_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = "__all__"


# Serializer for the product create.
class ProductCreate_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

    def validate(self, attrs):
        product_name = attrs.get("name")
        product_price = attrs.get("user_price")
        # here we have to check if the product is already exists or not.
        product_data = Product.objects.all()
        for product in product_data:
            if product_name == product.name:
                # here we have to extract the id of the product.
                product_id = Product.objects.get(name=product_name)
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


# catogery list for the product including certain data.
class CatogeryStock_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Catogery
        fields = ("id", "name")


# suppilier list for the product including certain data.
class SuppliersStock_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ("id", "name")


# Serializer for the product for the admin.
class ProductAdmin_Serializer(serializers.ModelSerializer):
    catogery = CatogeryStock_Serializer()
    supplier = SuppliersStock_Serializer()

    class Meta:
        model = Product
        fields = "__all__"


# Serializer for the product for the user.
class ProductUser_Serializer(serializers.ModelSerializer):
    catogery = CatogeryStock_Serializer()

    class Meta:
        model = Product
        exclude = [
            "created_at",
            "updated_at",
            "supplier",
        ]


# Serializer for the product.
class Product_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


# Serializer for the stock create.
class StockCreate_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = "__all__"

    def validate(self, attrs):
        qtn = attrs.get("quantity")
        if qtn == 0:
            raise serializers.ValidationError(
                {"msg": "In Stock you cannt put the quantity 0"}
            )
        return attrs


# Serializer for the stock for the admin.
class StockAdmin_Serializer(serializers.ModelSerializer):
    product = ProductAdmin_Serializer()

    class Meta:
        model = Stock
        fields = "__all__"


# Serializer for the total price for the stock.
class StockTotalPrice_Serializer(serializers.ModelSerializer):
    stock_total_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    class Meta:
        model = Stock
        exclude = [
            "product",
            "home_price",
            "quantity",
            "total_price",
        ]


# Serializer for the table.
class Table_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = "__all__"
