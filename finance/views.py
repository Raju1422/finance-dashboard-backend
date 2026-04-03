from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Record,Category
from .serializers import CategorySerializer,RecordSerializer
# Create your views here.
class RecordListCreateView(generics.ListCreateAPIView):
    serializer_class = RecordSerializer
    permission_classes = [IsAuthenticated]

    # def get_queryset(self):
    #     return Record.objects.filter(
    #         user=self.request.user,
    #         is_deleted=False
    #     )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)