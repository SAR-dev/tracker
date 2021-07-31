from rest_framework import serializers
from .models import Category
from expense.models import Expense
from django.contrib.auth import get_user_model
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']
        
class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id', 'title', 'description', 'amount', 'date']

class CategoryCreateSerializer(serializers.ModelSerializer):
    slug = serializers.ReadOnlyField()
    author = UserSerializer(read_only=True)
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'color', 'author', 'about', 'created_at', 'updated_at']


class CategoryListSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'color', 'author', 'about', 'created_at', 'updated_at']
        
class CategorySummarySerializer(serializers.ModelSerializer):
    category_expenses = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'color', 'about', 'category_expenses', 'created_at', 'updated_at']
        
    def get_category_expenses(self, obj):
        expenses = ExpenseSerializer(Expense.objects.filter(category__id = obj.id).all(), many=True)
        return expenses.data


class CategoryReriveSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'color', 'author', 'about', 'created_at', 'updated_at']


class CategoryUpdateSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'color', 'author', 'about', 'created_at', 'updated_at']
