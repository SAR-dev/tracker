from django.urls import path
from .views import ExpenseListView, ExpenseCreateView, ExpenseRetriveView, ExpenseUpdateView

app_name="expense"

urlpatterns = [
    path('', ExpenseListView.as_view(), name='expense-list'),
    path('create/', ExpenseCreateView.as_view(), name='expense-create'),
    path('<int:pk>/', ExpenseRetriveView.as_view(), name='expense-retrive'),
    path('<int:pk>/update/', ExpenseUpdateView.as_view(), name='expense-update'),
]