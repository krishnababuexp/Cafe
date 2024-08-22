from . import views
from django.urls import path

urlpatterns = [
    path(
        "bill/create/",
        views.BillCreateApiView.as_view(),
        name="path to create the bill for the admin",
    ),
    path(
        "bill/list/",
        views.BillListApiView.as_view(),
        name="path to see the list of the bills",
    ),
    path(
        "indivisual-print/details/<int:pk>/",
        views.BillPrintIndivisualApiView.as_view(),
        name="path to get the data for the print",
    ),
    path(
        "bill-order/list/",
        views.BillNOrderApiView.as_view(),
        name="path to see the order n bill on the particular date",
    ),
]
