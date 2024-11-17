from django.urls import path
from .views import SignupView, LoginView, OTPVerificationView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/otp/', LoginView.as_view(), name='otp-login'),
    path('login/verify/', OTPVerificationView.as_view(), name='otp-verify'),
]
