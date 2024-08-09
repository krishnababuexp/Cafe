from django.shortcuts import render
from .models import Catogery, Supplier, Stock
from cafe.render import UserRenderer
from rest_framework.views import APIView
from rest_framework import status, permissions, generics
from rest_framework.response import Response
from .serializer import (
    Catogery_Serializer,
    Suppliers_Serializer,
    StockCreate_Serializer,
    StockAdmin_Serializer,
    StockUser_Serializer,
    Stock_Serializer,
    StockTotalPrice_Serializer,
)
from cafe.pagination import MyPageNumberPagination
from django.shortcuts import get_object_or_404
from rest_framework.filters import SearchFilter
from django.db.models import Sum, F


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


# Stock.
# creating the stock.
class StockCreateApiView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, *args, **kwargs):
        serializer = StockCreate_Serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # here we check the quantity and calculate the total price.
            qtn = serializer.validated_data["quantity"]
            if qtn == 0:
                serializer.validated_data["total_price"] = 0
                serializer.save()
            else:
                hprice = serializer.validated_data["home_price"]
                stock_price = hprice * qtn
                print(stock_price)
                serializer.validated_data["total_price"] = stock_price
                serializer.save()
            return Response(
                {
                    "msg": "Product is added in the stock",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


# listing the stok for the admin only.
class StockListAdminApiView(generics.ListAPIView):
    renderer_classes = [UserRenderer]
    permission_classes = [permissions.IsAdminUser]
    queryset = Stock.objects.all().order_by("-id")
    serializer_class = StockAdmin_Serializer
    pagination_class = MyPageNumberPagination


# listing the stock for the normal user.
class StockListUserApiView(generics.ListAPIView):
    renderer_classes = [UserRenderer]
    permission_classes = [permissions.AllowAny]
    queryset = Stock.objects.all()
    serializer_class = StockUser_Serializer
    pagination_class = MyPageNumberPagination


# deleting the stock.
class StockDeleteApiView(generics.DestroyAPIView):
    renderer_classes = [UserRenderer]
    permission_classes = [permissions.IsAdminUser]
    queryset = Stock.objects.all()
    serializer_class = Stock_Serializer


# indivisual stock retrival for the update.
class IndivisualStockRetrivalApiView(generics.RetrieveAPIView):
    renderer_classes = [UserRenderer]
    permission_classes = [permissions.IsAdminUser]
    serializer_class = Stock_Serializer

    def get_object(self):
        id = self.kwargs.get("pk")
        return get_object_or_404(Stock, id=id)


# stock search for the admin or user.
class StockSearchApiView(generics.ListAPIView):
    renderer_classes = [UserRenderer]
    permission_classes = [permissions.AllowAny]
    serializer_class = Stock_Serializer
    queryset = Stock.objects.all().order_by("-id")
    filter_backends = [SearchFilter]
    search_fields = ["^name", "^catogery__name", "^supplier__name"]


# updating the stock for the admin.
class StockUpdateApiView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [permissions.IsAdminUser]

    def put(self, request, *args, **kwargs):
        id = self.kwargs.get("pk")
        stock_data = get_object_or_404(Stock, id=id)
        old_quantity = stock_data.quantity
        print(old_quantity)
        serializer = Stock_Serializer(stock_data, data=request.data)
        if serializer.is_valid(raise_exception=True):
            new_quantity = serializer.validated_data["quantity"]
            if old_quantity != new_quantity:
                hprice = serializer.validated_data["home_price"]
                print(hprice)
                stock_price = hprice * new_quantity
                serializer.validated_data["total_price"] = stock_price
                serializer.save()
            else:
                serializer.save()
            return Response(
                {
                    "msg": "The stock is sucessfully updated.",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


# total price of the stock.
class TotalPriceStockApiView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        total_prices = 0
        total_prices = Stock.objects.aggregate(total_prices=Sum(F("total_price")))
        serializer = StockTotalPrice_Serializer(
            {"stock_total_price": total_prices["total_prices"]}
        )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
