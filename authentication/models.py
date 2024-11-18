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
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(phone, email, password, **extra_fields)

class UserSignUP(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('consumer', 'Consumer'),
        ('tricycler', 'Tricycler'),
    ]

    first_name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    role = models.CharField(max_length=200, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=200, unique=True)
    hostel = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    email = models.EmailField(unique=True)
    photo = models.ImageField(upload_to='users/photo/',default='No Photo')
    password = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',  # Add a unique related_name for groups
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',  # Add a unique related_name for permissions
        blank=True
    )

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['email', 'first_name', 'surname']

    objects = UserManager()

    def __str__(self):
        return f"{self.first_name} {self.surname} ({self.phone})"

