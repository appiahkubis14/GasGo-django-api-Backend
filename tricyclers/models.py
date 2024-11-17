

from django.db import models
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Tricycler(models.Model):
    ROLE_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
    ]
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    address = models.TextField()
    vehicle_number = models.CharField(max_length=20, unique=True)
    status = models.CharField(max_length=10, choices=ROLE_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.vehicle_number})"

class Assignment(models.Model):
    tricycler = models.ForeignKey(Tricycler, on_delete=models.CASCADE, related_name='assignments')
    task_description = models.TextField()
    assigned_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Task for {self.tricycler.first_name} - {self.task_description[:20]}"



class TricyclerLocation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="location")
    latitude = models.FloatField()
    longitude = models.FloatField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.surname} - {self.latitude}, {self.longitude}"
