from django.urls import path
from .views import MerchantView
# from rest_framework.routers import DefaultRouter

# app_name = "Merchant"

urlpatterns = [
    path('', MerchantView.as_view(), name='merchant')
]