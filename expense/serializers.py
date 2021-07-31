from rest_framework import serializers
from .models import Expense
from category.models import Category
from django.contrib.auth import get_user_model
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class CategorySerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'color', 'author', 'about']

class ExpenseCreateSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)
    class Meta:
        model = Expense
        fields = ['id', 'title', 'description', 'amount', 'date', 'category', 'creator', 'created_at', 'updated_at']


class ExpenseListSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    creator = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    class Meta:
        model = Expense
        fields = ['id', 'title', 'description', 'amount', 'date', 'category', 'creator', 'created_at', 'updated_at']


class ExpenseReriveSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    creator = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    class Meta:
        model = Expense
        fields = ['id', 'title', 'description', 'amount', 'date', 'category', 'creator', 'created_at', 'updated_at']


class ExpenseUpdateSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)
    class Meta:
        model = Expense
        fields = ['id', 'title', 'description', 'amount', 'date', 'category', 'creator', 'created_at', 'updated_at']
