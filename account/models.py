from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
import os
from cafe.validation import (
    isalphanumericalvalidator,
    isalphavalidator,
    iscontactvalidator,
)


# CUSTOME USER MANAGER:
class UserManager(BaseUserManager):
    def create_user(
        self,
        email,
        first_name,
        last_name,
        phone,
        username,
        role,
        photo=None,
        password=None,
        password2=None,
        # **extra_fields,
    ):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            username=username,
            phone=phone,
            photo=photo,
            role=role,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        email,
        username,
        password,
        first_name,
        last_name,
        phone,
        role="admin",
        **extra_fields,
    ):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            role=role,
        )
        user.is_admin = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)


# Create your models here.
class User(AbstractBaseUser):
    USER_TYPE = (
        ("admin", "Admin"),
        ("staff", "Staff"),
        ("user", "user"),
    )
    email = models.EmailField(
        verbose_name="E-mail",
        max_length=255,
        unique=True,
    )
    photo = models.ImageField(
        # upload_to=category_image_dir_path,
        blank=True,
        null=True,
    )
    first_name = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        validators=[isalphavalidator],
    )
    last_name = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        validators=[isalphavalidator],
    )
    username = models.CharField(
        max_length=50,
        unique=True,
        blank=False,
        null=False,
        validators=[isalphanumericalvalidator],
    )
    phone = models.PositiveBigIntegerField(
        blank=True,
        null=True,
        validators=[iscontactvalidator],
    )
    role = models.CharField(
        max_length=100,
        choices=USER_TYPE,
        blank=True,
        null=True,
    )  # can be change according to the project progress.
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name", "phone"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
