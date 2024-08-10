from django.shortcuts import render
from .models import Order
from rest_framework.views import APIView
from rest_framework import generics, status, permissions
from cafe.render import UserRenderer
from cafe.pagination import MyPageNumberPagination
from .serializer import OrderCreate_Serializer


# Order.
# creating the order.
class OrderCreateApiView(generics.CreateAPIView):
    renderer_classes = [UserRenderer]
    permission_classes = [permissions.AllowAny]
    queryset = Order.objects.all()
    serializer_class = OrderCreate_Serializer
