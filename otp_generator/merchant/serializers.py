from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Merchant


class MerchantSerializer(ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Merchant
        fields = ['name', 'merchant_id', 'password', 'password2', 'website']
        # extra_kwargs = {
        #     'password': {'write_only': True}
        # }

    def save(self):
        merchant = Merchant(
            name=self.validated_data['name'],
            merchant_id=self.validated_data['merchant_id'],
            website=self.validated_data['website'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match'})
        merchant.save()
        return merchant
