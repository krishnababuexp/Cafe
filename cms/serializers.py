from rest_framework import serializers
from .models import CafeCms


class CmsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CafeCms
        fields = "__all__"
