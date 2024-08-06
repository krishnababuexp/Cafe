from rest_framework import serializers
from account.models import User
from cafe.utils import Util
from django.utils.encoding import DjangoUnicodeDecodeError, force_bytes, smart_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator


# user registrtion serializer.
class UserRegistration_Serializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style={"input_type": "password", "write_only": True}
    )

    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        password = attrs.get("password")
        password2 = attrs.get("password2")
        if password != password2:
            raise serializers.ValidationError(
                "Oops! It seems like the passwords don't match. Please double-check and try again."
            )
        return super().validate(attrs)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


# userlogin serializer.
class UserLogin_Serializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ["email", "password"]


# login user profile serializer.
class UserProfile_Serializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"


# user password change serializer.
class UserPasswordChange_Serializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=255, style={"input_type": "password"}, write_only=True
    )
    password2 = serializers.CharField(
        max_length=255, style={"input_type": "password"}, write_only=True
    )

    class Meta:
        model = User
        fields = ["password", "password2"]

    def validate(self, attrs):
        password = attrs.get("password")
        password2 = attrs.get("password2")
        user = self.context.get("user")
        if password != password2:
            raise serializers.ValidationError(
                {
                    "msg": "Oops! The passwords you entered don't match. Please try again."
                }
            )
        user.set_password(password)
        user.save()
        # email send after the password is changed.
        data = {
            "subject": "Password Change Notification",
            "body": f"Hi {user.first_name},\n\n"
            "We wanted to inform you that your password has been successfully updated on our platform. "
            "Your account security is our top priority, and we appreciate your diligence in keeping your "
            "information secure.\n\n"
            "If you did not authorize this change or have any concerns about your account security, "
            "please contact our support team immediately.\n\n"
            "Thank you for choosing our service!\n\n"
            "Best regards,\n"
            "Black Jack",
            "to_email": user.email,
        }
        Util.send_email(data)
        return attrs


# sending the reset email to the user.
class SendPasswordEmail_Serializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ["email"]

    def validate(self, attrs):
        email = attrs.get("email")
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print(uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print("the token is:", token)
            link = "http://127.0.0.1:3000/user/reset/" + uid + "/" + token
            print(link)
            # sending the mail to the user to change the password
            body = (
                "Hello there,\n\n"
                "You've requested to reset your password. To proceed, please click on the link below:\n\n"
                f"{link}\n\n"
                "If you didn't request this, you can safely ignore this email.\n\n"
                "Best regards,\n"
                "The Black Jack Team"
            )
            data = {
                "subject": "Password Reset Request",
                "body": body,
                "to_email": user.email,
            }
            Util.send_email(data)
            return attrs
        else:
            raise serializers.ValidationError("Oops! We couldn't find your email.")


# user password change serializer through the mail.
class UserPasswordReset_Serializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=255, style={"input_type": "password"}, write_only=True
    )
    password2 = serializers.CharField(
        max_length=255, style={"input_type": "password"}, write_only=True
    )

    class Meta:
        model = User
        fields = ["password", "password2"]

    def validate(self, attrs):
        try:
            password = attrs.get("password")
            password2 = attrs.get("password2")
            uid = self.context.get("uid")
            token = self.context.get("token")
            if password != password2:
                raise serializers.ValidationError(
                    "Oops! Your password confirmation doesn't match. Please double-check and try again."
                )
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError(
                    "Oops! Looks like something went wrong. Please refresh the page and try again. If the issue persists, please contact support for assistance."
                )
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise serializers.ValidationError(
                "Oops! It looks like there's an issue with your token. "
                "It may be invalid or expired. Please double-check your token "
                "and try again. If you continue to experience issues, "
                "please contact our support team for assistance."
            )


# login user profile update serializer.
class UserProfileUpdate_Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
