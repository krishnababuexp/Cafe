from django.urls import path
from . import views

urlpatterns = [
    path(
        "catogery/create/",
        views.CatogeryCreateApiView.as_view(),
        name="path to create the category",
    ),
    path(
        "catogery/list/",
        views.CatogeryListApiView.as_view(),
        name="path to see all the list of catogery",
    ),
    path(
        "catogery/update/<int:pk>/",
        views.CatogeryUpdateApiView.as_view(),
        name="path to update the catogery",
    ),
    path(
        "catogery/delete/<int:pk>/",
        views.CatogeryDeleteApiView.as_view(),
        name="path to delete the catogery",
    ),
    path(
        "catogery/indivisul-retrival/<int:pk>/",
        views.SingleCatogeryApiView.as_view(),
        name="path to get the single catogery",
    ),
    path(
        "catogery/search/",
        views.SerachCatogeryApiView.as_view(),
        name="path to search the catogery",
    ),
    # Suppliers.
    path(
        "suppliers/create/",
        views.SupplierCreateApiView.as_view(),
        name="path to create the suppliers",
    ),
    path(
        "suppliers/list/",
        views.SupplierListApiView.as_view(),
        name="path to see all the list of suppliers",
    ),
    path(
        "suppliers/update/<int:pk>/",
        views.SuppliersUpdateApiView.as_view(),
        name="path to update the suppliers",
    ),
    path(
        "suppliers/delete/<int:pk>/",
        views.SuppliersDeleteApiView.as_view(),
        name="path to delete the suppliers",
    ),
    path(
        "suppliers/indivisul-retrival/<int:pk>/",
        views.SingleSuppliersApiView.as_view(),
        name="path to get the single suppliers",
    ),
    path(
        "suppliers/search/",
        views.SerachSuppliersApiView.as_view(),
        name="path to search the suppliers",
    ),
]
