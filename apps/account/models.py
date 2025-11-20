from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.hashers import make_password  # hash
from django.contrib.auth.models import AbstractUser, UserManager, PermissionsMixin
from django.db.models.signals import post_save
from phonenumber_field.modelfields import PhoneNumberField

from config import settings


class CustomUserManager(UserManager):

    def _create_user(self, email, phone_number, password, username=None, **extra_fields):

        if not phone_number:
            raise ValueError("The given phone_number must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, phone_number=phone_number, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number, password=None, username=None, **extra_fields):  # Обычный пользователь
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(phone_number=phone_number, password=password, email=None, username=username,
                                 **extra_fields)

    def create_superuser(self, phone_number, email=None, password=None, username=None, **extra_fields):  # super user
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields["is_active"] = True

        if extra_fields.get("is_active") is not True:
            raise ValueError("Superuser must have is_active=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(phone_number=phone_number, email=None, password=password, username=username,
                                 **extra_fields)

class CustomUser(AbstractUser, PermissionsMixin):
    ACCOUNT_CHOICES = (
        ("admin", "админ"),
        ("chef", "шеф"),
        ("administrator", "администратор"),
        ("employee", "ученик"),
        ("client", "клиент"),
    )

    username = models.CharField(blank=True, null=True, max_length=150, verbose_name='Имя пользователя')
    phone_number = PhoneNumberField(null=False, blank=True, unique=True)
    is_active = models.BooleanField(default=True)
    email = models.EmailField(verbose_name='E-mail', null=True, blank=True)
    roles = models.CharField(choices=ACCOUNT_CHOICES, max_length=255, default="employee", verbose_name='Тип')
    rate = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(10.0)], default=7.0)
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ["username", ]
    is_rate_active = models.BooleanField(default=False)
    practice = models.BooleanField(default=False)
    balance_of_user = models.PositiveIntegerField(default=0)
    theme_order = models.CharField(max_length=250, blank=True, null=True, default="unusual_bg_blue")
    country = models.ForeignKey(
        to="Country",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Страна"
    )

    def __str__(self):
        return self.username




class Country(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name="Страна")
    code_password = models.CharField(max_length=20, verbose_name="Код доступа")

    class Meta:
        verbose_name = "Страна"
        verbose_name_plural = "Страны"

    def __str__(self):
        return f"{self.name} ({self.code_password})"



