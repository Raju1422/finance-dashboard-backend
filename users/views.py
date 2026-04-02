from rest_framework import generics
from .models import Role,User
from .serializers import RoleSerializer,UserSerializer,CustomTokenSerializer,UserRetrieveUpdateSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .permissions import IsAdmin    

class RoleListAPIView(generics.ListAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

class UserListCreateAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]

class LoginAPIView(TokenObtainPairView):
    serializer_class = CustomTokenSerializer


class UserRetrieveUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserRetrieveUpdateSerializer
    permission_classes = [IsAdmin]