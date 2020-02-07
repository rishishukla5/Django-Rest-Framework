import random
import string
import redis

from django.core.cache import cache
from django.core import cache
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from func_timeout import func_timeout, FunctionTimedOut
from django.db import connections
from django.db.utils import OperationalError

from .models import OTP
from .serializers import OTPSerializer

redis_django = redis.Redis(host='localhost', port=6379, db=0)


class OTPView(APIView):

    def generate(self, serializer, uuid):
        otp = serializer.save()
        random_otp = RandomOTP()
        otp.otp_generated = random_otp.generate()
        otp.save()
        redis_django.setex(otp.user_id, 60, otp.otp_generated)
        content = {
            "UUID": uuid,
            "User ID": otp.user_id,
            "OTP ": otp.otp_generated,

        }

        return Response(content, status=status.HTTP_201_CREATED)

    def validate(self, data):
        user_id = data['user_id']
        # If the user_id is present in cache, check if the OTP is valid or not.
        if user_id in redis_django:
            otp = redis_django.get(user_id)
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
        uuid = request.GET['UUID']
        if serializer.is_valid():
            # If the OTP field is not present in the POST request, we need to send an OTP
            if 'otp_generated' not in request.data.keys():
                # If the OTP has already been generated and hasn't expired yet, return it from the cache
                if request.data['user_id'] in redis_django:
                    otp = redis_django.get(request.data['user_id'])
                    content = {
                        "UUID": uuid,
                        "User ID": request.data['user_id'],
                        "OTP ": otp,

                    }
                    return Response(content, status=status.HTTP_200_OK)
                # If the OTP isn't present in the cache, generate an OTP and return
                else:
                    # If the user is present in the database and not in cache, delete the user from the database
                    queryset = OTP.objects.filter(user_id=request.data['user_id'])
                    if queryset:
                        queryset.delete()
                    return self.generate(serializer, uuid)  # Generating OTP
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
        if data['user_id'] in redis_django:
            redis_django.delete(data['user_id'])  # Deleting user from the cache
        return Response(data="Delete", status=status.HTTP_410_GONE)


class HealthStatusView(APIView):

    def redis_status(self):
        redis_health = "Working Fine"
        try:
            temp = func_timeout(0.0001, redis_django.ping)
        except FunctionTimedOut:
            redis_health = "Timeout"
        return redis_health

    def sql_status(self):
        db_conn = connections['default']
        try:
            c = db_conn.cursor()
        except OperationalError:
            return "Not Alive"
        else:
            return "Alive"

    def get(self, request):
        redis_health = self.redis_status()
        sql_health = self.sql_status()
        final_status = {
            "Redis": redis_health,
            "SQL": sql_health
        }
        return Response(final_status, status=status.HTTP_200_OK)


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
