
# tricyclers/serializers.py

from rest_framework import serializers
from .models import Tricycler, Assignment

class TricyclerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tricycler
        fields = '__all__'

class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = '__all__'
