from django.shortcuts import render
from .serializers import MerchantSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Merchant
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token


# Create your views here.
class MerchantView(APIView):
    # permission_classes = (IsAuthenticated,)

    # queryset = Merchant.objects.all()
    # serializer_class = MerchantSerializer
    def get_object(self):
        try:
            return Merchant.objects.all()
        except Merchant.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request):
        queryset = self.get_object()
        serializer = MerchantSerializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = MerchantSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            merchant = serializer.save()
            data['response'] = "Successfully Registered Merchant"
            data['merchant_id'] = merchant.merchant_id
            data['name'] = merchant.name
            # token = Token.objects.get(user=merchant).key
            token, _ = Token.objects.get_or_create(user=merchant)
            data['token'] = token
        else:
            data = serializer.errors
        return Response(data)

    def delete(self, request):
        queryset = Merchant.objects.get(id=4)
        queryset.delete()
        return Response(data="Delete", status=status.HTTP_410_GONE)
