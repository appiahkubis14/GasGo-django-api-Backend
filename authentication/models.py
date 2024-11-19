from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, phone, email, password=None, **extra_fields):
        if not phone:
            raise ValueError("Phone number is required")
        if not email:
            raise ValueError("Email is required")
        
        email = self.normalize_email(email)
        user = self.model(phone=phone, email=email, **extra_fields)

        if password:
            user.set_password(password)
        else:
            raise ValueError("Password is required")

        user.save(using=self._db)
        return user

    def create_superuser(self, phone, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(phone, email, password, **extra_fields)


class UserSignUP(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Consumer', 'Consumer'),
        ('Tricycler', 'Tricycler'),
    ]

    first_name = models.CharField(max_length=200, blank=True, null=True)
    surname = models.CharField(max_length=200,blank=True, null=True)
    role = models.CharField(max_length=200, choices=ROLE_CHOICES,blank=True, null=True)
    phone = models.CharField(max_length=200, unique=True,blank=True, null=True)
    hostel = models.CharField(max_length=500, blank=True, null=True)
    address = models.TextField(max_length=200, blank=True, null=True)
    email = models.EmailField(unique=True,blank=True, null=True)
    photo = models.ImageField(upload_to='users/photo/', default='users/photo/default.png')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        'auth.Group',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        blank=True
    )

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['email', 'first_name', 'surname']

    objects = UserManager()

    def __str__(self):
        return f"{self.first_name} {self.surname} ({self.phone})"
