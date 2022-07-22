from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import TaskList, TaskDetail,\
    TaskEdit, TaskDelete, TaskCreate, CustomLogin, Register


urlpatterns = [
    path('login/', CustomLogin.as_view(), name='login'),
    path('register/', Register.as_view(), name='register'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('taskcreate/', TaskCreate.as_view(), name='taskcreate'),
    path('taskdelete/<int:pk>/', TaskDelete.as_view(), name='taskdelete'),
    path('taskedit/<int:pk>/', TaskEdit.as_view(), name='taskedit'),
    path('taskdetail/<int:pk>/', TaskDetail.as_view(), name='taskdetail'),
    path('', TaskList.as_view(), name='tasklist')
]
