from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status, permissions
from .models import Bill, Order
from rest_framework.response import Response
from cafe.render import UserRenderer
from cafe.pagination import MyPageNumberPagination
from rest_framework.filters import SearchFilter
from rest_framework.views import APIView
from bill.serializer import (
    BillCreate_Serializer,
    BillList_Serializer,
    BillDetail_Serializer,
)
from datetime import datetime
from cms.models import CafeCms
from django.db.models import Sum


def get_grand_total_price(total_price_order, dicounted_price, additional_amount):
    if additional_amount == None:
        grand_total_price = total_price_order - dicounted_price
    else:
        grand_total_price = (total_price_order + additional_amount) - dicounted_price
    return grand_total_price


def get_grand_total_price1(total_price_order, additional_amount):
    if additional_amount == None:
        grand_total_price = total_price_order
    else:
        grand_total_price = total_price_order + additional_amount
    return grand_total_price


# View for the bill ccreate.
class BillCreateApiView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, *args, **kwargs):
        print("i am in the post of the bill create")
        serializer = BillCreate_Serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            current_datetime = datetime.now()
            current_date = current_datetime.date()
            cafe = CafeCms.objects.first()
            name = cafe.name.lower().replace(" ", "-")
            ors = serializer.validated_data["order"]
            order = Order.objects.get(order_number=ors)
            bill_number = f"{current_date}{name}{ors}"
            final_bill_number = bill_number.replace("-", "")
            serializer.validated_data["bill_number"] = final_bill_number
            print(cafe.discount_rate)
            if cafe.discount_rate != None and cafe.discount_rate != 0:
                discount_rate = cafe.discount_rate
                total_price_order = order.total_price
                dicounted_price = (discount_rate / 100) * total_price_order
                serializer.validated_data["discount_amount"] = dicounted_price
                serializer.validated_data["discount_rate"] = discount_rate
                serializer.validated_data["grand_total"] = get_grand_total_price(
                    total_price_order, dicounted_price, cafe.additional_amount
                )
            else:
                serializer.validated_data["grand_total"] = get_grand_total_price1(
                    order.total_price, cafe.additional_amount
                )
            serializer.save()
            return Response(
                {"msg": "Bill sucesfully created", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


# view for the order list for the admin.
class BillListApiView(generics.ListAPIView):
    renderer_classes = [UserRenderer]
    permission_classes = [permissions.IsAdminUser]
    queryset = Bill.objects.all().order_by("-bill_created", "-bill_time")
    serializer_class = BillList_Serializer
    pagination_class = MyPageNumberPagination


# view to reterive the indivisual data and to ge the print out of the bill.
class BillPrintIndivisualApiView(generics.RetrieveAPIView):
    renderer_classes = [UserRenderer]
    permission_classes = [permissions.IsAdminUser]
    serializer_class = BillDetail_Serializer

    def get_object(self):
        id = self.kwargs.get("pk")
        return Bill.objects.get(id=id)


def get_time_based_data(date):
    try:
        bills_data = Bill.objects.filter(bill_created=date)
        total_price_sell = bills_data.aggregate(Sum("grand_total"))
        total_number_bill_payed = bills_data.count()
        total_number_oreder = Order.objects.filter(order_date=date).count()
        serializer = BillDetail_Serializer(bills_data, many=True)
        response_data = {
            "total_price_sell": total_price_sell,
            "total_number_bill_payed": total_number_bill_payed,
            "total_number_oreder": total_number_oreder,
            "data": serializer.data,
        }
        return response_data
    except ValueError:
        return Response(
            {"msg": "Invalid date format. Please use YYYY-MM-DD format."},
            status=status.HTTP_400_BAD_REQUEST,
        )


# view to see the bill list on the particular date and the orders too.
class BillNOrderApiView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        date = request.query_params.get("date", None)
        if date:
            return Response(
                get_time_based_data(date),
                status=status.HTTP_200_OK,
            )
        else:
            current_datetime = datetime.now()
            date = current_datetime.date()
            return Response(
                get_time_based_data(date),
                status=status.HTTP_200_OK,
            )
