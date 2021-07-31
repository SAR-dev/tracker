from django.db import models
from django.core.validators import RegexValidator
from utils.generators import generate_unique_slug
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
import os
from category.models import Category
from django.contrib.auth import get_user_model
User = get_user_model()
from django.utils import timezone

class Expense(models.Model):
    title = models.CharField(max_length=100)
    description= models.CharField(max_length=200, default=None, blank=True, null=True)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    date = models.DateTimeField(default=timezone.now)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category', default=None, blank=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator', default=None, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = models.Manager()
    
    def __str__(self):
        return str(self.title)
    
    class Meta:
        ordering = ['-id']
        