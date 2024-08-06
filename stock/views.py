from django.shortcuts import render
from .models import Catogery, Supplier
from cafe.render import UserRenderer
from rest_framework.views import APIView
from rest_framework import status, permissions, generics
from rest_framework.response import Response
from .serializer import Catogery_Serializer, Suppliers_Serializer
from cafe.pagination import MyPageNumberPagination
from django.shortcuts import get_object_or_404
from rest_framework.filters import SearchFilter


# Catogery.
# creating the catogery.
class CatogeryCreateApiView(generics.CreateAPIView):
    renderer_classes = [UserRenderer]
    permission_classes = [permissions.IsAdminUser]
    queryset = Catogery.objects.all()
    serializer_class = Catogery_Serializer


# displaying the list.
class CatogeryListApiView(generics.ListAPIView):
    renderer_classes = [UserRenderer]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Catogery.objects.all().order_by("-id")
    serializer_class = Catogery_Serializer
    pagination_class = MyPageNumberPagination


# updating the catogery.
class CatogeryUpdateApiView(generics.UpdateAPIView):
    renderer_classes = [UserRenderer]
    permission_classes = [permissions.IsAdminUser]
    queryset = Catogery.objects.all()
    serializer_class = Catogery_Serializer


# deleting the catogery.
class CatogeryDeleteApiView(generics.DestroyAPIView):
    renderer_classes = [UserRenderer]
    permission_classes = [permissions.IsAdminUser]
    serializer_class = Catogery_Serializer
    queryset = Catogery.objects.all()


# single catogery reterival.
class SingleCatogeryApiView(generics.RetrieveAPIView):
    renderer_classes = [UserRenderer]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = Catogery_Serializer

    def get_object(self):
        id = self.kwargs.get("pk")
        return get_object_or_404(Catogery, id=id)


# searching the catogery.
class SerachCatogeryApiView(generics.ListAPIView):
    renderer_classes = [UserRenderer]
    serializer_class = Catogery_Serializer
    queryset = Catogery.objects.all().order_by("-id")
    filter_backends = [SearchFilter]
    search_fields = ["^name"]
    pagination_class = MyPageNumberPagination


# Suppliers.
# creating the suppliers.
class SupplierCreateApiView(generics.CreateAPIView):
    renderer_classes = [UserRenderer]
    permission_classes = [permissions.IsAdminUser]
    queryset = Supplier.objects.all()
    serializer_class = Suppliers_Serializer


# listing the suppliers.
class SupplierListApiView(generics.ListAPIView):
    renderer_classes = [UserRenderer]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Supplier.objects.all().order_by("-id")
    serializer_class = Suppliers_Serializer
    pagination_class = MyPageNumberPagination


# updating the suppliers.
class SuppliersUpdateApiView(generics.UpdateAPIView):
    renderer_classes = [UserRenderer]
    permission_classes = [permissions.IsAdminUser]
    queryset = Supplier.objects.all()
    serializer_class = Suppliers_Serializer


# deleting the suppliers.
class SuppliersDeleteApiView(generics.DestroyAPIView):
    renderer_classes = [UserRenderer]
    permission_classes = [permissions.IsAdminUser]
    serializer_class = Suppliers_Serializer
    queryset = Supplier.objects.all()


# single suppliers reterival.
class SingleSuppliersApiView(generics.RetrieveAPIView):
    renderer_classes = [UserRenderer]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = Suppliers_Serializer

    def get_object(self):
        id = self.kwargs.get("pk")
        return get_object_or_404(Supplier, id=id)


# searching the suppliers.
class SerachSuppliersApiView(generics.ListAPIView):
    renderer_classes = [UserRenderer]
    serializer_class = Suppliers_Serializer
    queryset = Supplier.objects.all().order_by("-id")
    filter_backends = [SearchFilter]
    search_fields = ["^name"]
    pagination_class = MyPageNumberPagination
