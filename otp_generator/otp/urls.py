from django.urls import path
from .views import OTPView, HealthStatusView

urlpatterns = [
    path('', OTPView.as_view(), name='otp_generate'),
    path('status/', HealthStatusView.as_view(), name='status'),
]
