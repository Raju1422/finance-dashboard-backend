from rest_framework import generics
from .models import Category,Record
from .serializers import CategorySerializer,RecordSerializer,RecordDetailSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import RecordPermission
from rest_framework.views import APIView   
from django.db.models import Sum
from django.db.models.functions import TruncMonth,TruncWeek
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import SearchFilter
from datetime import datetime
from rest_framework.exceptions import ValidationError


class CategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes =[IsAuthenticated]

class RecordListCreateAPIView(generics.ListCreateAPIView):
    queryset = Record.objects.filter(is_deleted=False)
    serializer_class = RecordSerializer
    permission_classes = [IsAuthenticated,RecordPermission] 
    filter_backends = [SearchFilter]
    search_fields = ['description', 'category__name', 'user__email']
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = Record.objects.filter(is_deleted=False)

        date = self.request.query_params.get('date')
        category = self.request.query_params.get('category')
        type_ = self.request.query_params.get('type')

        if date:
            try:
                parsed_date = datetime.strptime(date, "%Y-%m-%d").date()
                queryset = queryset.filter(date=parsed_date)
            except ValueError:
                raise ValidationError({"date": "Invalid date format. Use YYYY-MM-DD"})

        if category:
            queryset = queryset.filter(category_id=category)

        if type_:
            if type_ not in ['income', 'expense']:
                raise ValidationError({"type": "Invalid type. Must be 'income' or 'expense'"})
            queryset = queryset.filter(category__type=type_)

        return queryset

class RecordRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Record.objects.filter(is_deleted=False)
    serializer_class = RecordDetailSerializer
    permission_classes = [IsAuthenticated,RecordPermission]
   

    def perform_destroy(self, instance):
        instance.is_deleted = True  
        instance.save()


class DashboardAPIView(APIView):
    permission_classes =[IsAuthenticated]

    def get(self,request):
        records = Record.objects.filter(is_deleted=False)

        #total income 
        total_income = records.filter(category__type='income').aggregate(
            total=Sum('amount')
        )['total'] or 0

        #total expense
        total_expense =  records.filter(category__type='expense').aggregate(
            total=Sum('amount')
        )['total'] or 0

        # Net Balance
        net_balance = total_income - total_expense

        # category-wise totals
        category_data = records.values('category__name').annotate(
            total=Sum('amount')
        )
        
        #recent activity
        recent_records = records.order_by('-created_at')[:5].values(
            'id',
            'amount',
            'category__name',
            'category__type',
            'date',
            'description'
        )

        #monthly trends
        monthly_trends = records.annotate(month=TruncMonth('date')).values('month', 'category__type').annotate(
            total=Sum('amount')
        ).order_by('month')

        # weekly trends
        weekly_trends = records.annotate(week=TruncWeek('date')).values('week', 'category__type').annotate(
            total=Sum('amount')
        ).order_by('week')
        
        return Response({
            "total_income": total_income,
            "total_expense": total_expense,
            "net_balance": net_balance,
            "category_breakdown": list(category_data),
            "recent_records": list(recent_records),
            "monthly_trends": list(monthly_trends),
            "weekly_trends": list(weekly_trends)
        }, status=status.HTTP_200_OK)


