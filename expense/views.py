from .models import Expense
from category.models import Category
from utils.paginations import PazeSizePagination
from rest_framework import generics, views, response, permissions, exceptions, status
from django.shortcuts import get_object_or_404
from django.core.serializers import serialize
from rest_framework.exceptions import NotFound
from django.core.exceptions import ObjectDoesNotExist
from .serializers import ExpenseCreateSerializer, ExpenseListSerializer, ExpenseReriveSerializer, ExpenseUpdateSerializer
from django.contrib.auth import get_user_model
User = get_user_model()
from django_filters import rest_framework as filters


class IsAuthor(permissions.BasePermission):
    message = 'Only author has access!'

    def has_permission(self, request, view):
        try:
            obj = Expense.objects.get(pk=view.kwargs.get('pk'))
            return obj.creator.id == request.user.id
        except ObjectDoesNotExist:
            raise NotFound(detail="Error 404, Not Found!", code=404)
        
class IsAuthorOfCategory(permissions.BasePermission):
    message = 'Only author has access!'

    def has_permission(self, request, view):
        try:
            obj = Category.objects.get(slug=view.kwargs.get('slug'))
            return obj.author.id == request.user.id
        except ObjectDoesNotExist:
            raise NotFound(detail="Error 404, Not Found!", code=404)
        

class ExpenseFilter(filters.FilterSet):
    o = filters.OrderingFilter(
        fields=(
            ('title', 'title'),
            ('description', 'description'),
            ('date', 'date'),
            ('created_at', 'created_at'),
        ),
    )

    class Meta:
        model = Expense
        fields = {
            'title': ['icontains'],
            'description': ['icontains'],
            'category__slug': ['exact'],
            'date': ['exact', 'gt', 'lt'],
        }

class ExpenseListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ExpenseListSerializer
    filterset_class = ExpenseFilter

    def get_queryset(self):
        try:
            return Expense.objects.filter(creator = self.request.user.id)
        except ObjectDoesNotExist:
            raise NotFound(detail="Error 404, Not Found!", code=404)
       
class ExpenseCreateView(generics.CreateAPIView):
    def perform_create(self, serializer):
        try:
            if Category.objects.get(pk = self.request.data['category']).author == self.request.user :
                serializer.save(creator = self.request.user)
            else:
                raise NotFound(
                    detail="Error 404, Selected category not found!", code=404)
        except ObjectDoesNotExist:
            raise NotFound(
                    detail={"category" : "Error 404, Selected category not found!"}, code=404)

    permission_classes = [permissions.IsAuthenticated]
    queryset = Expense.objects.all()
    serializer_class = ExpenseCreateSerializer

class ExpenseRetriveView(generics.RetrieveAPIView):
    permission_classes = [IsAuthor]
    serializer_class = ExpenseReriveSerializer
    queryset = Expense.objects.all()
    
class ExpenseUpdateView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthor]
    serializer_class = ExpenseReriveSerializer
    queryset = Expense.objects.all()