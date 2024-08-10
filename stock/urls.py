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
    # Product.
    path(
        "product/create/",
        views.ProductCreateApiView.as_view(),
        name="path to create the product",
    ),
    path(
        "product/alist/",
        views.ProductListAdminApiView.as_view(),
        name="path to see the list of the product for the admin",
    ),
    path(
        "product/ulist/",
        views.ProductListUserApiView.as_view(),
        name="path to see the list of the product for the user",
    ),
    path(
        "product/delete/<int:pk>/",
        views.ProductDeleteApiView.as_view(),
        name="path to delete the product for the admin.",
    ),
    path(
        "indivisula/product-retrival/<int:pk>/",
        views.IndivisualProductRetrivalApiView.as_view(),
        name="path to get the indivisual product for the update.",
    ),
    path(
        "product/search/",
        views.ProductSearchApiView.as_view(),
        name="path to search the product from the database",
    ),
    path(
        "product/update/<int:pk>/",
        views.ProductUpdateApiView.as_view(),
        name="path to update the product for the admin.",
    ),
    # Table
    path(
        "table/create/",
        views.TableCreateApiView.as_view(),
        name="path to create the table",
    ),
    path(
        "table/list/",
        views.TableListApiView.as_view(),
        name="path to see all the list of table",
    ),
    path(
        "table/update/<int:pk>/",
        views.TableUpdateApiView.as_view(),
        name="path to update the table",
    ),
    path(
        "table/delete/<int:pk>/",
        views.TableDeleteApiView.as_view(),
        name="path to delete the table",
    ),
    path(
        "table/indivisul-retrival/<int:pk>/",
        views.SingleTableApiView.as_view(),
        name="path to get the single table",
    ),
    path(
        "table/search/",
        views.SerachTableApiView.as_view(),
        name="path to search the table",
    ),
    # Stock.
    path(
        "stock/create/",
        views.StockCreateApiView.as_view(),
        name="path to create the stock",
    ),
    path(
        "stock/list/",
        views.StockListApiView.as_view(),
        name="path to see the stock list",
    ),
    path(
        "stock/search/",
        views.SearchStockApiView.as_view(),
        name="path to search the stock from the database",
    ),
    path(
        "indivisula/stock-retrival/<int:pk>/",
        views.IndivisualStockApiView.as_view(),
        name="path to get the indivisual stock for the update.",
    ),
    path(
        "stock/delete/<int:pk>/",
        views.StockDeleteApiView.as_view(),
        name="path to delete the stock for the admin.",
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
