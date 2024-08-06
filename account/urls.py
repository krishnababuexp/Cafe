from django.urls import path
from . import views

urlpatterns = [
    path(
        "user/registration/",
        views.UserRegistrationView.as_view(),
        name="path to register the user.",
    ),
    path(
        "user/login/",
        views.UserLoginView.as_view(),
        name="path to login the user",
    ),
    path(
        "login/user/profile/",
        views.UserProfileView.as_view(),
        name="path to see the login user profile",
    ),
    path(
        "login/user/password-change/",
        views.UserPasswordChangeView.as_view(),
        name="path to change the password when the user is login",
    ),
    path(
        "user/password-change/link/",
        views.SendPassowrdEmailView.as_view(),
        name="path to send the user the link to change the password",
    ),
    path(
        "user/reset-password/",
        views.UserPasswordResetView.as_view(),
        name="path to reset the passsword",
    ),
    path(
        "user/profile-update/",
        views.LoginUserProfileUpdateApiView.as_view(),
        name="path to update the profile of the login user",
    ),
]
