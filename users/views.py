from rest_framework import generics
from .models import Role,User
from .serializers import RoleSerializer,UserSerializer,CustomTokenSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class RoleListAPIView(generics.ListAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

class UserListCreateAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class LoginAPIView(TokenObtainPairView):
    serializer_class = CustomTokenSerializer