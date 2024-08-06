from rest_framework import serializers
from .models import Catogery


# Serializer for the Catogery.
class Catogery_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Catogery
        fields = "__all__"
