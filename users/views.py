from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.views import (
    TokenObtainPairView
)

from users.serializers import CustomTokenObtainPairSerializer, UserSerializer

class UserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data) 
        if serializer.is_valid():
            serializer.save()
            return Response({'message':' 가입완료!'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message':f'${serializer.errors}'}, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class=CustomTokenObtainPairSerializer
    
class mockView(APIView): 
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        return Response('get 요청!')
    