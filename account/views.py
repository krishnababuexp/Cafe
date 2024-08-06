from django.shortcuts import render
from rest_framework.views import APIView
from cafe.render import UserRenderer
from .serializer import (
    UserRegistration_Serializer,
    UserLogin_Serializer,
    UserProfile_Serializer,
    UserPasswordChange_Serializer,
    SendPasswordEmail_Serializer,
    UserPasswordReset_Serializer,
    UserProfileUpdate_Serializer,
)
from rest_framework import status, generics, permissions
from cafe.token_generate import get_tokens_for_user
from rest_framework.response import Response
from django.contrib.auth import authenticate
from cafe.utils import Util
from django.shortcuts import get_object_or_404
from account.models import User

# Create your views here.


# user registration view.
class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserRegistration_Serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            uid = user.id
            data = {
                "subject": "Welcome to Our Community!",
                "body": f"Dear {user.first_name},\n\n"
                "Congratulations! You've successfully registered on our platform.\n\n"
                "Best regards,\n"
                "The EPS Team",
                "to_email": user.email,
            }
            Util.send_email(data)
            token = get_tokens_for_user(user)
            return Response(
                {
                    "token": token,
                    "msg": "Registration Successful",
                    "uid": uid,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


# user login view.
class UserLoginView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserLogin_Serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get("email")
            password = serializer.data.get("password")
            user = authenticate(email=email, password=password)
            print(user)
            if user is not None:
                uid = user.id
                user_type = user.is_admin
                token = get_tokens_for_user(user)
                return Response(
                    {
                        "token": token,
                        "user_is_admin": user_type,
                        "msg": "Login Successfully",
                        "id": uid,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"msg": "Email or Password is not valide"},
                    status=status.HTTP_404_NOT_FOUND,
                )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


# login user profile view.
class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        serializer = UserProfile_Serializer(request.user)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


# user password change view.
class UserPasswordChangeView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        serializer = UserPasswordChange_Serializer(
            data=request.data, context={"user": request.user}
        )
        if serializer.is_valid(raise_exception=True):
            return Response(
                {"msg": "Password changed Sucessfully"},
                status=status.HTTP_200_OK,
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


# sending the email to the user to change the password.
class SendPassowrdEmailView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = SendPasswordEmail_Serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(
                {"msg": "Passwoed Reset link send. Please check your Email"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# user password change view through the mail.
class UserPasswordResetView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, uid, token, format=None):
        serializer = UserPasswordReset_Serializer(
            data=request.data, context={"uid": uid, "token": token}
        )
        if serializer.is_valid(raise_exception=True):
            return Response({"msg": "Password Reset Sucessfully"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# login user profile update path.
class LoginUserProfileUpdateApiView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, *args, **kwargs):
        user = request.user.id
        user_data = get_object_or_404(User, id=user)
        serializer = UserProfileUpdate_Serializer(
            user_data,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )
