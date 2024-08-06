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
]
