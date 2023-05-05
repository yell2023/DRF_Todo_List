from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from todo.models import Todo
from todo.serializers import TodoSerializer,TodoListSerializer,TodoCreateSerializer

class TodoListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request): # 본인 todo 전체 리스트 조회
        todo_list = Todo.objects.filter(user_id=request.user)
        serializer = TodoListSerializer(todo_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def post(self, request): # todo 작성
        serializer = TodoCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user) 
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TodoListDetailView(APIView): # todo 상세보기
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request,id): 
        todo = get_object_or_404(Todo, id=id)
        serializer = TodoSerializer(todo)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request,id): # todo 수정
        todo = get_object_or_404(Todo, id=id)
        serializer = TodoCreateSerializer(todo, data=request.data)
        if request.user == todo.user:
            if serializer.is_valid():
                serializer.save() 
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('권한이 없습니다!', status=status.HTTP_403_FORBIDDEN)
    
    def delete(self, request,id): # todo 삭제
        todo = get_object_or_404(Todo, id=id)
        if request.user == todo.user:
            todo.delete()
            return Response('삭제되었습니다!', status=status.HTTP_204_NO_CONTENT)
        else:
            return Response('권한이 없습니다!', status=status.HTTP_403_FORBIDDEN)    