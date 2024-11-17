from django.contrib import admin
from .models import Consumer

@admin.register(Consumer)
class ConsumerAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'surname', 'phone', 'email', 'created_at')
    search_fields = ('first_name', 'surname', 'phone', 'email')
