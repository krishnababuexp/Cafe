from django.shortcuts import render
from .models import Catogery, Supplier, Product, Table, Stock
from cms.models import CafeCms
from cafe.render import UserRenderer
from rest_framework.views import APIView
from rest_framework import status, permissions, generics
from rest_framework.response import Response
from django.http import JsonResponse
from .serializer import (
    CatogeryCreate_Serializer,
    Catogery_Serializer,
    Suppliers_Serializer,
    ProductCreate_Serializer,
    ProductAdmin_Serializer,
    ProductUser_Serializer,
    Product_Serializer,
    StockTotalPrice_Serializer,
    Table_Serializer,
    StockCreate_Serializer,
    StockAdmin_Serializer,
)
from cafe.pagination import MyPageNumberPagination
from django.shortcuts import get_object_or_404
from rest_framework.filters import SearchFilter
from django.db.models import Sum, F
import os
from django.db import transaction
from django.core.management.base import BaseCommand
from cafe.utils import Util


# Catogery.
# creating the catogery.
class CatogeryCreateApiView(generics.CreateAPIView):
    renderer_classes = [UserRenderer]
    permission_classes = [permissions.IsAdminUser]
    queryset = Catogery.objects.all()
    serializer_class = CatogeryCreate_Serializer


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
    serializer_class = CatogeryCreate_Serializer

    # # here we check if the catogery image is updated or not if updated then we delete the old image.
    # def perform_update(self, serializer):
    #     instance = self.get_object()
    #     old_photo_path = instance.photo.path if instance.photo else None
    #     super().perform_update(serializer)
    #     instance.refresh_from_db()
    #     if old_photo_path != instance.photo.path:
    #         if os.path.exists(old_photo_path):
    #             os.remove(old_photo_path)


# deleting the catogery.
class CatogeryDeleteApiView(generics.DestroyAPIView):
    renderer_classes = [UserRenderer]
    permission_classes = [permissions.IsAdminUser]
    serializer_class = Catogery_Serializer
    queryset = Catogery.objects.all()
    # here we have to delete the catogery image if the catogery is deleted.

    # def destroy(self, request, *args, **kwargs):
    #     instance = get_object_or_404(Catogery, pk=kwargs["pk"])
    #     photo_path_in_folder = instance.photo.path
    #     if photo_path_in_folder and os.path.isfile(photo_path_in_folder):
    #         os.remove(photo_path_in_folder)
    #     return super().destroy(request, *args, **kwargs)


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


# product.
# creating the product.
class ProductCreateApiView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, *args, **kwargs):
        serializer = ProductCreate_Serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {
                    "msg": "Product is added in Sucessfully",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


# listing the product for the admin only.
class ProductListAdminApiView(generics.ListAPIView):
    renderer_classes = [UserRenderer]
    permission_classes = [permissions.IsAdminUser]
    queryset = Product.objects.all().order_by("-id")
    serializer_class = ProductAdmin_Serializer
    pagination_class = MyPageNumberPagination


# listing the product for the normal user.
class ProductListUserApiView(generics.ListAPIView):
    renderer_classes = [UserRenderer]
    permission_classes = [permissions.AllowAny]
    queryset = Product.objects.all()
    serializer_class = ProductUser_Serializer
    pagination_class = MyPageNumberPagination


# deleting the product.
class ProductDeleteApiView(generics.DestroyAPIView):
    renderer_classes = [UserRenderer]
    permission_classes = [permissions.IsAdminUser]
    queryset = Product.objects.all()
    serializer_class = Product_Serializer

    # # here delete the image of the stock is also deleted.
    # def destroy(self, request, *args, **kwargs):
    #     instance = get_object_or_404(Product, pk=kwargs["pk"])
    #     photo_path = instance.photo.path
    #     if photo_path and os.path.isfile(photo_path):
    #         os.remove(photo_path)
    #     return super().destroy(request, *args, **kwargs)


# indivisual product retrival for the update.
class IndivisualProductRetrivalApiView(generics.RetrieveAPIView):
    renderer_classes = [UserRenderer]
    permission_classes = [permissions.IsAdminUser]
    serializer_class = Product_Serializer

    def get_object(self):
        id = self.kwargs.get("pk")
        return get_object_or_404(Product, id=id)


# product search for the admin or user.
class ProductSearchApiView(generics.ListAPIView):
    renderer_classes = [UserRenderer]
    permission_classes = [permissions.AllowAny]
    serializer_class = Product_Serializer
    queryset = Product.objects.all().order_by("-id")
    filter_backends = [SearchFilter]
    search_fields = ["^name", "^catogery__name", "^supplier__name"]


# # updating the product for the admin.
# class ProductUpdateApiView(APIView):
#     renderer_classes = [UserRenderer]
#     permission_classes = [permissions.IsAdminUser]

#     def put(self, request, *args, **kwargs):
#         id = self.kwargs.get("pk")
#         product_data = get_object_or_404(Product, id=id)
#         old_quantity = product_data.quantity
#         old_photo_path = product_data.photo.path if product_data.photo else None
#         serializer = Product_Serializer(product_data, data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             new_quantity = serializer.validated_data["quantity"]
#             if old_quantity != new_quantity:
#                 hprice = serializer.validated_data["home_price"]
#                 print(hprice)
#                 stock_price = hprice * new_quantity
#                 serializer.validated_data["total_price"] = stock_price
#                 # serializer.save()
#                 # calling the perform_update operation to update the image.
#                 self.perform_update(serializer, old_photo_path)
#             else:
#                 # serializer.save()
#                 self.perform_update(serializer, old_photo_path)
#             return Response(
#                 {
#                     "msg": "The stock is sucessfully updated.",
#                     "data": serializer.data,
#                 },
#                 status=status.HTTP_200_OK,
#             )
#         return Response(
#             serializer.errors,
#             status=status.HTTP_400_BAD_REQUEST,
#         )

#     def perform_update(self, serializer, old_photo_path):
#         serializer.save()
#         instance = serializer.instance
#         print(old_photo_path)
#         print(instance.photo.path)
#         if old_photo_path and instance.photo.path != old_photo_path:
#             if os.path.exists(old_photo_path):
#                 os.remove(old_photo_path)


# updating the product for the admin.
class ProductUpdateApiView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [permissions.IsAdminUser]
    queryset = Product.objects.all()
    serializer_class = Product_Serializer


# Stock.
# creating the stock.
class StockCreateApiView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, *args, **kwargs):
        serializer = StockCreate_Serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            qtn = serializer.validated_data["initial_quantity"]
            price = serializer.validated_data["home_price"]
            total_price = qtn * price
            serializer.validated_data["initial_quantity_price"] = total_price
            serializer.validated_data["remaining_quantity"] = qtn
            serializer.validated_data["remaining_quantity_total_price"] = total_price
            serializer.save()
            return Response(
                {
                    "msg": "Stock Added Sucessfully",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


# listing the stock for the admin.
class StockListApiView(generics.ListAPIView):
    renderer_classes = [UserRenderer]
    permission_classes = [permissions.IsAdminUser]
    queryset = Stock.objects.all().order_by("-created_at")
    serializer_class = StockAdmin_Serializer
    pagination_class = MyPageNumberPagination


# searching the stock for the admin.
class SearchStockApiView(generics.ListAPIView):
    renderer_classes = [UserRenderer]
    permission_classes = [permissions.IsAdminUser]
    serializer_class = StockAdmin_Serializer
    queryset = Stock.objects.all().order_by("created_at")
    filter_backends = [SearchFilter]
    search_fields = ["^product__name"]
    pagination_class = MyPageNumberPagination


# indivisual stock retrival.
class IndivisualStockApiView(generics.RetrieveAPIView):
    renderer_classes = [UserRenderer]
    permission_classes = [permissions.IsAdminUser]
    serializer_class = StockAdmin_Serializer

    def get_object(self):
        id = self.kwargs.get("pk")
        return get_object_or_404(Stock, id=id)


# deleting the stock.
class StockDeleteApiView(generics.DestroyAPIView):
    renderer_classes = [UserRenderer]
    permission_classes = [permissions.IsAdminUser]
    queryset = Stock.objects.all()
    serializer_class = StockAdmin_Serializer


# updating the stock.
class StockUpdateApiView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [permissions.AllowAny]

    def put(self, request, *args, **kwargs):
        id = self.kwargs.get("pk")
        stock_data = get_object_or_404(Stock, id=id)
        old_home_price = stock_data.home_price
        serializer = StockCreate_Serializer(stock_data, data=request.data)

        if serializer.is_valid(raise_exception=True):
            new_qtn = serializer.validated_data.get("added_quantity", 0)
            new_home_price = serializer.validated_data.get("home_price", old_home_price)

            with transaction.atomic():
                if new_qtn > 0:
                    added_quantity_price = new_qtn * old_home_price
                    new_initial_quantity = stock_data.remaining_quantity + new_qtn
                    new_initial_quantity_price = new_initial_quantity * old_home_price
                    serializer.validated_data.update(
                        {
                            "added_quantity_price": added_quantity_price,
                            "initial_quantity": new_initial_quantity,
                            "initial_quantity_price": new_initial_quantity_price,
                            "remaining_quantity": new_initial_quantity,
                            "remaining_quantity_total_price": new_initial_quantity_price,
                        }
                    )
                    serializer.save()
                if old_home_price != new_home_price:
                    remaining_quantity_price = (
                        stock_data.remaining_quantity * new_home_price
                    )
                    initial_quantity_price = (
                        stock_data.initial_quantity * new_home_price
                    )
                    added_quantity = serializer.validated_data.get("added_quantity", 0)
                    if added_quantity == 0:
                        added_quantity_price = stock_data.added_quantity_price
                    else:
                        added_quantity_price = (
                            added_quantity * new_home_price if added_quantity else 0
                        )

                    serializer.validated_data.update(
                        {
                            "remaining_quantity_total_price": remaining_quantity_price,
                            "initial_quantity_price": initial_quantity_price,
                            "added_quantity_price": added_quantity_price,
                        }
                    )
                    serializer.save()

                serializer.save()

            return Response(
                {
                    "msg": "Stock has been updated.",
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
        remaining_total_prices = 0
        total_prices = Stock.objects.aggregate(
            total_prices=Sum(F("initial_quantity_price"))
        )
        remaining_total_prices = Stock.objects.aggregate(
            remaining_total_prices=Sum(F("remaining_quantity_total_price"))
        )
        serializer = StockTotalPrice_Serializer(
            {
                "overall_stock_total_price": total_prices["total_prices"],
                "remaining_stock_total_price": remaining_total_prices[
                    "remaining_total_prices"
                ],
            }
        )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


# Table.
# creating the table.
class TableCreateApiView(generics.CreateAPIView):
    renderer_classes = [UserRenderer]
    permission_classes = [permissions.IsAdminUser]
    queryset = Table.objects.all()
    serializer_class = Table_Serializer


# displaying the list of the table.
class TableListApiView(generics.ListAPIView):
    renderer_classes = [UserRenderer]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Table.objects.all().order_by("-table_number")
    serializer_class = Table_Serializer
    pagination_class = MyPageNumberPagination


# updating the table.
class TableUpdateApiView(generics.UpdateAPIView):
    renderer_classes = [UserRenderer]
    permission_classes = [permissions.IsAdminUser]
    queryset = Table.objects.all()
    serializer_class = Table_Serializer


# deleting the table.
class TableDeleteApiView(generics.DestroyAPIView):
    renderer_classes = [UserRenderer]
    permission_classes = [permissions.IsAdminUser]
    serializer_class = Table_Serializer
    queryset = Table.objects.all()


# single table reterival.
class SingleTableApiView(generics.RetrieveAPIView):
    renderer_classes = [UserRenderer]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = Table_Serializer

    def get_object(self):
        id = self.kwargs.get("pk")
        return get_object_or_404(Table, id=id)


# searching the table.
class SerachTableApiView(generics.ListAPIView):
    renderer_classes = [UserRenderer]
    serializer_class = Table_Serializer
    queryset = Table.objects.all().order_by("-table_number")
    filter_backends = [SearchFilter]
    search_fields = ["^table_name"]
    pagination_class = MyPageNumberPagination


# here we define the threeshold for the stock product quantity.
def calulate_threeshold(product_quantity):
    if product_quantity >= 750:
        return 40
    elif product_quantity >= 500:
        return 30
    elif product_quantity >= 200:
        return 25
    elif product_quantity >= 100:
        return 20
    elif product_quantity >= 10:
        return 5
    else:
        return 2


# view to send the mail to the admin if the stock is low.
def send_email_handle(self):
    low_stock_products = []

    for stock_product in Stock.objects.all():
        threshold = calulate_threeshold(stock_product.remaining_quantity)
        if stock_product.remaining_quantity <= threshold:
            low_stock_products.append(stock_product)

        if low_stock_products:
            product_list = "\n".join(
                [f"{sp.product}: {sp.remaining_quantity}" for sp in low_stock_products]
            )
            admin_user = CafeCms.objects.first()
            admin_user_emails = [
                email
                for email in [
                    admin_user.email_1,
                    admin_user.cafe_email,
                    admin_user.email_2,
                ]
                if email is not None
            ]

            for user in admin_user_emails:
                data = {
                    "subject": "Alert: The stock quantity for some products is critically low!",
                    "body": (
                        f"Dear Admin,\n\nThe following products have low stock levels:\n\n"
                        f"{product_list}\n\n"
                        "Best regards,\n"
                        "The Black Jack Application"
                    ),
                    "to_email": user,
                }
                try:
                    Util.send_email(data)
                except Exception as e:
                    # Log the exception and continue
                    print(f"Error sending email to {user}: {e}")

            return JsonResponse(
                {"message": "mail has been delivered..."},
                status=status.HTTP_200_OK,
            )
        # else:
        #     return JsonResponse(
        #         {"msg": "No low stock products found."},
        #         status=status.HTTP_200_OK,
        #     )
