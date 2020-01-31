from rest_framework.views import APIView
from .models import Question, Quiz
from rest_framework.response import Response
from rest_framework import status
from .serializers import QuizSerializer, QuestionSerializer
from rest_framework import generics
from rest_framework import viewsets


# class QuizView(APIView):
#
#     def get_object(self):
#         try:
#             return Quiz.objects.all()
#         except Quiz.DoesNotExist:
#             raise status.HTTP_404_NOT_FOUND
#
#     def get(self, request):
#         queryset = self.get_object()
#         serializer = QuizSerializer(queryset, many=True)
#         return Response(data=serializer.data, status=status.HTTP_200_OK)
#
#     def post(self, request):
#         serializer = QuizSerializer(data=request.data)
#         try:
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#         except Exception as e:
#             print(e)
#             return Response(serializer.error_messages, status=status.HTTP_404_NOT_FOUND)
#
#     def delete(self, request):
#         queryset = Quiz.objects.get(id=3)
#         queryset.delete()
#         return Response(data="Delete", status=status.HTTP_410_GONE)
#
#     def put(self, request):
#         quiz = Quiz.objects.get(id=request.data['id'])
#         serializer = QuizSerializer(quiz, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(data=serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_410_GONE)

class QuizView(generics.ListCreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
#     lookup_field = 'pk'

# class QuizView(viewsets.ModelViewSet):
#     queryset = Quiz.objects.all
#     serializer_class = QuizSerializer
