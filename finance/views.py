from rest_framework import generics
from .models import Category,Record
from .serializers import CategorySerializer,RecordSerializer,RecordDetailSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import RecordPermission   

class CategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes =[IsAuthenticated]

class RecordListCreateAPIView(generics.ListCreateAPIView):
    queryset = Record.objects.filter(is_deleted=False)
    serializer_class = RecordSerializer
    permission_classes = [IsAuthenticated,RecordPermission] 

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = Record.objects.filter(is_deleted=False)

        # 🔍 Get query params
        date = self.request.query_params.get('date')
        category = self.request.query_params.get('category')
        type_ = self.request.query_params.get('type')

        if date:
            queryset = queryset.filter(date=date)

        if category:
            queryset = queryset.filter(category_id=category)

        if type_:
            queryset = queryset.filter(category__type=type_)

        return queryset

class RecordRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Record.objects.filter(is_deleted=False)
    serializer_class = RecordDetailSerializer
    permission_classes = [IsAuthenticated,RecordPermission]

    def perform_destroy(self, instance):
        instance.is_deleted = True  
        instance.save()