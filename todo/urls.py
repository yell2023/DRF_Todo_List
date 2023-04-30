from django.urls import path
from todo import views

urlpatterns = [
    path('',views.TodoListView.as_view(), name='todo_list_view'), 
    path('<int:id>/',views.TodoListDetailView.as_view(), name='todo_list__detail_view'), 
]