from django.shortcuts import render
from .serializers import OTPSerializer
from rest_framework import generics
from rest_framework.response import Response
from .models import OTP
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

# Create your views here.
class OTPView(APIView):
    permission_classes = (IsAuthenticated,)
    queryset = OTP.objects.all()
    serializer_class = OTPSerializer
    # def get(self, request):
    #     content = {'message': 'Hello, World!'}
    #     return Response(content)
