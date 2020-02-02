from django.shortcuts import render
from .serializers import OTPSerializer
from rest_framework import generics
from rest_framework.response import Response
from .models import OTP
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
import string, random
from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


# Create your views here.
class OTPView(APIView):
    queryset = OTP.objects.all()
    serializer_class = OTPSerializer

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)

    def random_otp(self, blacklisted_otps):
        value = ""
        while True:
            for i in range(6):
                value += random.choice(string.ascii_letters + string.digits)
            if value not in blacklisted_otps:
                return value
            else:
                value = ""

    def post(self, request):
        serializer = OTPSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            otp = serializer.save()
            blacklisted_otps = ['123456', 'ABC123', '000000', '999999']
            otp.otp_generated = self.random_otp(blacklisted_otps)
            cache.set(otp.user_id, otp.otp_generated, timeout=CACHE_TTL)
            data['user_id'] = otp.user_id
            data['otp_generated'] = otp.otp_generated
            data = serializer.errors
        return Response(data)


class ResendOTP(APIView):

    def post(self, request):
        data = request.data
        user_id = data['user_id']
        if user_id in cache:
            otp = cache.get(user_id)
            return Response(otp, status=status.HTTP_201_CREATED)

