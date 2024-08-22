from django.shortcuts import render, get_object_or_404
from .models import Order, OrderItem, Table, Product, Stock
from rest_framework.views import APIView
from rest_framework import generics, status, permissions
from cafe.render import UserRenderer
from cafe.pagination import MyPageNumberPagination
from .serializer import (
    OrderCreate_Serializer,
    OrderList_Serializer,
    OrderListAdmin_Serializer,
    OrderItemUpdateSerializer,
    OrderUpdateSerializer,
)
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from datetime import datetime


# Order.
# creating the order.
class OrderCreateApiView(generics.CreateAPIView):
    renderer_classes = [UserRenderer]
    permission_classes = [permissions.IsAdminUser]
    queryset = Order.objects.all()
    serializer_class = OrderCreate_Serializer


# here i want to retrive the order detial according to the table number.
class OrderTableList(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        order = (
            Order.objects.filter(table_number__table_number=pk)
            .order_by("-order_date", "-order_time")
            .first()
        )
        serializer = OrderListAdmin_Serializer(order)
        return Response(serializer.data)


# deleting the orderitem from the order.
class OrderItemDeleteApiView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, order_number, pk, *args, **kwargs):
        order_data = get_object_or_404(Order, order_number=order_number)
        try:
            order_item_present = OrderItem.objects.get(order=order_data, id=pk)
        except OrderItem.DoesNotExist:
            return Response(
                {
                    "msg": f"The order item id {pk} doesnt match in the order",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        order_item_present.delete()
        # Recalculate and update the total price of the order
        quantity_order_list = order_item_present.quantity
        product_order_list = order_item_present.product
        product_data = get_object_or_404(Product, id=product_order_list.id)
        price_reduced = product_data.user_price * quantity_order_list
        order_data.total_price -= price_reduced
        order_data.save()

        # Update the stock quantity if the product is in stock
        stock_data = Stock.objects.filter(product=product_order_list).first()
        if stock_data:
            stock_data.quantity += quantity_order_list
            stock_data.save()

        return Response(
            {
                "msg": f"Order item id {pk} was successfully deleted from order {order_number}.",
            },
            status=status.HTTP_204_NO_CONTENT,
        )


# deleting the whole order.
class OrderDeleteApiView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, order_number, table_number, *args, **kwargs):
        table = get_object_or_404(Table, table_number=table_number)
        try:
            order_data = Order.objects.get(
                order_number=order_number, table_number=table
            )
        except Order.DoesNotExist:
            return Response(
                {
                    "msg": f"The order with the order number {order_number} doesnot exits."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        order_data.delete()
        table.available = True
        table.save()
        return Response(
            {
                "msg": f"Order with order number {order_number} was successfully deleted.",
            },
            status=status.HTTP_204_NO_CONTENT,
        )


# orderitem update view.
class OrderItemUpdateApiView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, table_number, order_number, pk, *args, **kwargs):
        table = get_object_or_404(Table, table_number=table_number)
        # checking of the order is present in the table and the order exist or not.
        try:
            order_present = Order.objects.get(
                table_number=table, order_number=order_number
            )
        except Order.DoesNotExist:
            return Response(
                {"msg": "Order not found for the given table and order number."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # checking if the order item exists or not.
        try:
            order_item_present = OrderItem.objects.get(order=order_present, id=pk)
        except OrderItem.DoesNotExist:
            return Response(
                {"msg": "Order item not found in the specified order."},
                status=status.HTTP_404_NOT_FOUND,
            )
        serilaizer = OrderUpdateSerializer(order_present, data=request.data)
        if serilaizer.is_valid(raise_exception=True):
            serilaizer.save()
            return Response(
                {
                    "msg": f"The order item has been updated sucessfully",
                    "data": serilaizer.data,
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            serilaizer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


# order search view.
class OrderSerachApiView(generics.ListAPIView):
    renderer_classes = [UserRenderer]
    permission_classes = [permissions.IsAdminUser]
    serializer_class = OrderListAdmin_Serializer
    queryset = Order.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ["^order_number"]
    pagination_class = MyPageNumberPagination


# order list based on the time.
class OrderListTimeApiView(generics.ListAPIView):
    renderer_classes = [UserRenderer]
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        date = request.query_params.get("date", None)
        if date:
            try:
                order_date = datetime.strptime(date, "%Y-%m-%d").date()
                orders = Order.objects.filter(order_date=order_date)
                print(orders)
            except ValueError:
                return Response(
                    {"msg": "Invalid date format. Please use YYYY-MM-DD format."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            orders = Order.objects.all().order_by("-order_date")
        serializer = OrderListAdmin_Serializer(orders, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
