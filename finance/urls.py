from django.urls import path
from .views import CategoryListCreateAPIView,RecordListCreateAPIView,RecordRetrieveUpdateDestroyAPIView,DashboardAPIView

urlpatterns = [
    path('categories/', CategoryListCreateAPIView.as_view(), name='category-list-create'),
    path('records/', RecordListCreateAPIView.as_view(), name='record-list-create'),
    path('records/<int:pk>/', RecordRetrieveUpdateDestroyAPIView.as_view(), name='record-detail'),
    path('dashboard/', DashboardAPIView.as_view(), name='dashboard'),
]