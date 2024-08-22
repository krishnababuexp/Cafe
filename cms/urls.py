from django.urls import path
from . import views


urlpatterns = [
    path(
        "cafe-cms/create/",
        views.CafeCmsCreateApiView.as_view(),
        name="path to create the cms.",
    ),
    path(
        "cafe-cms/list/",
        views.CafeCmsListApiView.as_view(),
        name="path to see the list of the cms",
    ),
    path(
        "cafe-cms/indivisual/detail/<int:pk>/",
        views.CafeCmsDetailApiView.as_view(),
        name="path to see the detail of the cms",
    ),
    path(
        "cafe-cms/delete/<int:pk>/",
        views.CafeCmsDeleteApiView.as_view(),
        name="path to delete the cms",
    ),
    path(
        "cafe-cms/update/<int:pk>/",
        views.CafeCmsUpdateApiView.as_view(),
        name="path to update the cms",
    ),
]
