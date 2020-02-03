import random
import string

from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import OTP
from .serializers import OTPSerializer

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class OTPView(APIView):

    def generate(self, serializer):
        otp = serializer.save()
        random_otp = RandomOTP()
        otp.otp_generated = random_otp.generate()
        otp.save()
        cache.set(otp.user_id, otp.otp_generated, timeout=CACHE_TTL)
        return Response(otp.otp_generated, status=status.HTTP_201_CREATED)

    def validate(self, data):
        user_id = data['user_id']
        # If the user_id is present in cache, check if the OTP is valid or not.
        if user_id in cache:
            otp = cache.get(user_id)
            if otp == data['otp_generated']:
                content = {"message": "OTP Validated Successfully"}
                return Response(content, status=status.HTTP_200_OK)
            else:
                content = {"message": "Incorrect OTP"}
                return Response(content, status=status.HTTP_403_FORBIDDEN)
        # Else, return that the user does not exist
        else:
            content = {"message": "User Does Not Exist"}
            return Response(content, status=status.HTTP_403_FORBIDDEN)

    def post(self, request):
        serializer = OTPSerializer(data=request.data)
        if serializer.is_valid():
            # If the OTP field is not present in the POST request, we need to send an OTP
            if 'otp_generated' not in request.data.keys():
                # If the OTP has already been generated and hasn't expired yet, return it from the cache
                if request.data['user_id'] in cache:
                    otp = cache.get(request.data['user_id'])
                    return Response(otp, status=status.HTTP_200_OK)
                # If the OTP isn't present in the cache, generate an OTP and return
                else:
                    # If the user is present in the database and not in cache, delete the user from the database
                    queryset = OTP.objects.filter(user_id=request.data['user_id'])
                    if queryset:
                        queryset.delete()
                    return self.generate(serializer)           # Generating OTP
            # Validate the OTP corresponding to the user_id present in the POST request
            else:
                return self.validate(request.data)
        # Return an error if the serializer is not valid
        else:
            return Response(serializer.errors)

    def delete(self, request):
        data = request.data
        queryset = OTP.objects.get(user_id=data['user_id'])
        queryset.delete()  # Deleting user from the database
        if data['user_id'] in cache:
            cache.delete(data['user_id'])  # Deleting user from the cache
        return Response(data="Delete", status=status.HTTP_410_GONE)


class RandomOTP:
    blacklisted_otps = ['123456', '000000', '999999']

    def generate(self):
        value = ""
        while True:
            for i in range(6):
                value += random.choice(string.digits)
            if value not in self.blacklisted_otps:
                return value
            else:
                value = ""
