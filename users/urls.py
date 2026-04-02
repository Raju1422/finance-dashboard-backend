from django.urls import path
from .views import RoleListAPIView,UserListCreateAPIView,LoginAPIView

urlpatterns = [
    path('roles/', RoleListAPIView.as_view()),
    path('users/', UserListCreateAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
]