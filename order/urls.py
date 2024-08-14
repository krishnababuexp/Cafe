from django.urls import path
from . import views

urlpatterns = [
    # Order.
    path(
        "order/create/",
        views.OrderCreateApiView.as_view(),
        name="path to create the order",
    ),
    path(
        "table-order/list/<int:pk>/",
        views.OrderTableList.as_view(),
        name="path to see the list of the table according to the tabel.",
    ),
    path(
        "ordered-item-delete/<str:order_number>/<int:pk>/",
        views.OrderItemDeleteApiView.as_view(),
        name="path to delete the order item from the order",
    ),
    path(
        "order/delete/<str:order_number>/<int:table_number>/",
        views.OrderDeleteApiView.as_view(),
        name="path to delete the order",
    ),
    path(
        "order-item-update/<int:table_number>/<str:order_number>/<int:pk>/",
        views.OrderItemUpdateApiView.as_view(),
        name="path to update the ordered item",
    ),
    path(
        "order/search/",
        views.OrderSerachApiView.as_view(),
        name="path to search the order",
    ),
]
