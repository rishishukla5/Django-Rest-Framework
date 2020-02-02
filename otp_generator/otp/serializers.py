from rest_framework.serializers import ModelSerializer
from .models import OTP


class OTPSerializer(ModelSerializer):
    class Meta:
        model = OTP
        fields = ['user_id']
