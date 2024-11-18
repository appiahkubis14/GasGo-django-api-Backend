from django.contrib.auth import authenticate
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.conf import settings
from random import randint
from rest_framework_simplejwt.tokens import RefreshToken
from .models import UserSignUP
from .serializers import SignupSerializer, OTPVerificationSerializer
from rest_framework.generics import get_object_or_404


class SignupView(APIView):
    """
    API View to handle user signup.
    """
    #post method
    def post(self, request):
        if request.method == 'POST':
            serializer = SignupSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                otp = randint(1000, 9999)  # Generate a random OTP
                user.otp = otp  # Assume `otp` is a field in the UserSignUP model
                user.is_active = False  # User remains inactive until OTP is verified
                user.save()

                try:
                    # Send OTP via email
                    send_mail(
                        subject="Your OTP for Account Verification",
                        message=f"Hello {user.first_name}, your OTP is {otp}.",
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[user.email],
                    )
                except Exception as e:
                    return Response(
                        {"error": "Failed to send OTP via email.", "details": str(e)},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )

                return Response(
                    {"message": "User created successfully. OTP sent to email."},
                    status=status.HTTP_201_CREATED,
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #get meethod
    def get(self , request,index):
        userInfo = get_object_or_404(UserSignUP , index)
        user_serializer = SignupSerializer(userInfo)
        return Response(user_serializer.data)

    #put method
    def put(self , request,index):
        userInfo = get_object_or_404(UserSignUP,index)
        user_serializer = SignupSerializer(userInfo,request.data,partial=True)
        if user_serializer.is_valid:
            user_serializer = user_serializer.save()
            return Response({"message": "User updated successfully"}, status=status.HTTP_200_OK)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #delete method
    def delete(self, request , index):
        userInfo = get_object_or_404(UserSignUP , index)
        return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


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

                    # Generate tokens for the user
                    refresh = RefreshToken.for_user(user)

                    return Response(
                        {
                            "message": "Verification successful. You can now log in.",
                            "tokens": {
                                "refresh": str(refresh),
                                "access": str(refresh.access_token),
                            },
                        },
                        status=status.HTTP_200_OK,
                    )
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
        email = request.data.get('email')

        user = authenticate(phone=phone, password=password, email=email)
        if user:
            # Generate tokens for the user
            refresh = RefreshToken.for_user(user)

            return Response(
                {
                    "message": "Login successful.",
                    "tokens": {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    },
                },
                status=status.HTTP_200_OK,
            )
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
