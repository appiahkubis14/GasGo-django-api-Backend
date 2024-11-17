from rest_framework import serializers
from .models import Consumer

class ConsumerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consumer
        fields = ['id', 'first_name', 'surname', 'phone', 'hostel', 'address', 'email', 'created_at', 'updated_at']
