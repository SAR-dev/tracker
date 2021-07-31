from .models import Category
from utils.paginations import PazeSizePagination
from rest_framework import generics, views, response, permissions, exceptions, status
from django.shortcuts import get_object_or_404
from django.core.serializers import serialize
from rest_framework.exceptions import NotFound
from django.core.exceptions import ObjectDoesNotExist
from .serializers import CategoryCreateSerializer, CategoryListSerializer, CategoryReriveSerializer, CategoryUpdateSerializer, CategorySummarySerializer
from django.contrib.auth import get_user_model
User = get_user_model()
from django_filters import rest_framework as filters


class IsAuthor(permissions.BasePermission):
    message = 'Only author has access!'

    def has_permission(self, request, view):
        try:
            obj = Category.objects.get(pk=view.kwargs.get('pk'))
            return obj.author.id == request.user.id
        except ObjectDoesNotExist:
            raise NotFound(detail="Error 404, Not Found!", code=404)
        

class CategoryFilter(filters.FilterSet):
    o = filters.OrderingFilter(
        fields=(
            ('name', 'name'),
            ('about', 'about'),
            ('created_at', 'created_at'),
        ),
    )

    class Meta:
        model = Category
        fields = {
            'name': ['icontains'],
            'about': ['icontains'],
        }

class CategoryListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CategoryListSerializer
    filterset_class = CategoryFilter

    def get_queryset(self):
        try:
            return Category.objects.filter(author = self.request.user.id)
        except ObjectDoesNotExist:
            raise NotFound(detail="Error 404, Not Found!", code=404)
        
class CategorySummaryView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CategorySummarySerializer
    filterset_class = CategoryFilter

    def get_queryset(self):
        try:
            return Category.objects.filter(author = self.request.user.id)
        except ObjectDoesNotExist:
            raise NotFound(detail="Error 404, Not Found!", code=404)
       
class CategoryCreateView(generics.CreateAPIView):
    def perform_create(self, serializer):
        serializer.save(author = self.request.user)

    permission_classes = [permissions.IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategoryCreateSerializer

class CategoryRetriveView(generics.RetrieveAPIView):
    permission_classes = [IsAuthor]
    serializer_class = CategoryReriveSerializer
    queryset = Category.objects.all()
    
class CategoryUpdateView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthor]
    serializer_class = CategoryReriveSerializer
    queryset = Category.objects.all()