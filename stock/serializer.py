from rest_framework import serializers
from .models import Catogery, Supplier


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
