from rest_framework import serializers
from .models import UserSignUP
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving user details.
    """
    class Meta:
        model = UserSignUP
        fields = ['id', 'first_name', 'surname', 'role', 'phone', 'hostel', 'address', 'email','password','photo']



class SignupSerializer(serializers.ModelSerializer):
    """
    Serializer for user signup with password hashing.
    """
    class Meta:
        model = UserSignUP
        fields = [
            'photo', 'first_name', 'surname', 'role', 'phone', 
            'hostel', 'address', 'email', 'password'
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Hash the password before saving the user
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class OTPVerificationSerializer(serializers.Serializer):
    """
    Serializer for OTP verification.
    """
    phone = serializers.CharField(max_length=10) 
    otp = serializers.CharField(max_length=4)
