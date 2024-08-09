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
    # STOCK.
    path(
        "stock/create/",
        views.StockCreateApiView.as_view(),
        name="path to create the stock",
    ),
    path(
        "stock/alist/",
        views.StockListAdminApiView.as_view(),
        name="path to see the list of the stock for the admin",
    ),
    path(
        "stock/ulist/",
        views.StockListUserApiView.as_view(),
        name="path to see the list of the stock for the user",
    ),
    path(
        "stock/delete/<int:pk>/",
        views.StockDeleteApiView.as_view(),
        name="path to delete the stock for the admin.",
    ),
    path(
        "indivisula/stock-retrival/<int:pk>/",
        views.IndivisualStockRetrivalApiView.as_view(),
        name="path to get the indivisual stock for the update.",
    ),
    path(
        "stock/search/",
        views.StockSearchApiView.as_view(),
        name="path to search the stock from the database",
    ),
    path(
        "stock/update/<int:pk>/",
        views.StockUpdateApiView.as_view(),
        name="path to update the stock for the admin.",
    ),
    path(
        "stock/total-price/",
        views.TotalPriceStockApiView.as_view(),
        name="patht to get the over all price of the stock.",
    ),
]
