from django.urls import path
from .views import OTPView

urlpatterns = [
    path('', OTPView.as_view(), name='otp_generate')
]
