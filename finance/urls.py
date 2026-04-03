from django.urls import path
from .views import CategoryListCreateAPIView,RecordListCreateAPIView,RecordRetrieveUpdateDestroyAPIView,DashboardAPIView

urlpatterns = [
    path('categories/', CategoryListCreateAPIView.as_view()),
    path('records/', RecordListCreateAPIView.as_view()),
    path('records/<int:pk>/', RecordRetrieveUpdateDestroyAPIView.as_view()),
    path('dashboard/', DashboardAPIView.as_view())
]