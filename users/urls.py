from django.urls import path
from .views import RoleListAPIView,UserListCreateAPIView,LoginAPIView,UserRetrieveUpdateAPIView

urlpatterns = [
    path('roles/', RoleListAPIView.as_view()),
    path('users/', UserListCreateAPIView.as_view()),
    path('users/<int:pk>/', UserRetrieveUpdateAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
]