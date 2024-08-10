from django.urls import path
from . import views

urlpatterns = [
    # Order.
    path(
        "order/create/",
        views.OrderCreateApiView.as_view(),
        name="path to create the order",
    ),
]
