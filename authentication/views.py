from django.contrib.auth import authenticate
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.conf import settings
from random import randint
from .models import UserSignUP
from .serializers import SignupSerializer, OTPVerificationSerializer


class SignupView(APIView):
    """
    API View to handle user signup.
    """
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            otp = randint(1000, 9999)
            user.otp = otp  # Assume `otp` is an additional field in the User model.
            user.save()

            # Send OTP via email
            send_mail(
                subject="Your OTP for Account Verification",
                message=f"Hello {user.first_name}, your OTP is {otp}.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
            )

            return Response({"message": "User created successfully. OTP sent to email."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OTPVerificationView(APIView):
    """
    API View to handle OTP verification.
    """
    def post(self, request):
        serializer = OTPVerificationSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data.get('phone')
            otp = serializer.validated_data.get('otp')

            try:
                user = UserSignUP.objects.get(phone=phone)
                if str(user.otp) == otp:  # Match OTP
                    user.otp = None  # Clear OTP after successful verification
                    user.is_active = True  # Activate the user account
                    user.save()

                    # Optionally, generate a token (e.g., using SimpleJWT)
                    return Response({"message": "Verification successful. You can now log in."}, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
            except UserSignUP.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    API View to handle user login.
    """
    def post(self, request):
        phone = request.data.get('phone')
        password = request.data.get('password')

        user = authenticate(phone=phone, password=password)
        if user:
            # Optionally, generate and return a token (e.g., using SimpleJWT)
            return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
