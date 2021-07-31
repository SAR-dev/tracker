from django.urls import path
from .views import CategoryListView, CategoryCreateView, CategoryRetriveView, CategoryUpdateView, CategorySummaryView

app_name="category"

urlpatterns = [
    path('', CategoryListView.as_view(), name='category-list'),
    path('create/', CategoryCreateView.as_view(), name='category-create'),
    path('summary/', CategorySummaryView.as_view(), name='category-summary'),
    path('<int:pk>/', CategoryRetriveView.as_view(), name='category-retrive'),
    path('<int:pk>/update/', CategoryUpdateView.as_view(), name='category-update'),
]