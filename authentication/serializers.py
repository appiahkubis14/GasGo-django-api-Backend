from rest_framework import serializers
from .models import UserSignUP


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving user details.
    """
    class Meta:
        model = UserSignUP
        fields = ['id', 'first_name', 'surname', 'role', 'phone', 'hostel', 'address', 'email','password','photo']


class SignupSerializer(serializers.ModelSerializer):
    """
    Serializer for user signup with validation for password.
    """
    class Meta:
        model = UserSignUP
        fields = ['photo','first_name', 'surname', 'role', 'phone', 'hostel', 'address', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """
        Creates a new user with the provided validated data.
        """
        return UserSignUP.objects.create_user(**validated_data)


class OTPVerificationSerializer(serializers.Serializer):
    """
    Serializer for OTP verification.
    """
    phone = serializers.CharField(max_length=10) 
    otp = serializers.CharField(max_length=4)
