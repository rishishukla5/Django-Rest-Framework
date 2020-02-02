from django.urls import path
from .views import OTPView, ResendOTP

urlpatterns = [
    path('', OTPView.as_view(), name='otp_generate'),
    path('resend/', ResendOTP.as_view(), name='otp_resend')
]
