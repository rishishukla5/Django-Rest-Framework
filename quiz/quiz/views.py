from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView


@api_view(['GET', 'POST'])
def index(request):
    print(request.user)
    print(request.auth)
    if request.method == 'GET':
        return Response(data='message1', status=status.HTTP_200_OK)
    elif request.method == 'POST':
        return Response(data=request.data, status=status.HTTP_200_OK)
    else:
        return Response(data='message3')


class Message(APIView):

    def get(self, request):
        return Response(data="This is a class based view hit by the get method.", status=status.HTTP_200_OK)

    def post(self, request):
        return Response(data="This is a class based view hit by the post method", status=status.HTTP_200_OK)
