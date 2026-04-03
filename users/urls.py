from django.urls import path
from .views import RoleListAPIView,UserListCreateAPIView,LoginAPIView,UserRetrieveUpdateAPIView

urlpatterns = [
    path('roles/', RoleListAPIView.as_view(), name='role-list'),
    path('', UserListCreateAPIView.as_view(), name='user-list-create'),
    path('<int:pk>/', UserRetrieveUpdateAPIView.as_view(), name='user-detail'),
    path('login/', LoginAPIView.as_view(), name='user-login'),
]