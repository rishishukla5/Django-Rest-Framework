from django.urls import path
from .views import QuizView
# from rest_framework.routers import DefaultRouter


urlpatterns = [
    path('quizzes/',QuizView.as_view(),name='quizzes')
]