from django.urls import path
from .views import FinanceHome
from . import views

urlpatterns = [
    path('', FinanceHome, name='finance_home'),
    path('accounts/', views.AccountListView.as_view(), name='finance_account_list'),
    path('accounts/new/', views.AccountCreateView.as_view(), name='finance_account_create'),
    path('accounts/<int:pk>/edit/', views.AccountUpdateView.as_view(), name='finance_account_edit'),
    path('accounts/<int:pk>/delete/', views.AccountDeleteView.as_view(), name='finance_account_delete'),
    path('categories/', views.CategoryListView.as_view(), name='finance_category_list'),
    path('categories/new/', views.CategoryCreateView.as_view(), name='finance_category_create'),
    path('categories/<int:pk>/edit/', views.CategoryUpdateView.as_view(), name='finance_category_edit'),
    path('categories/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='finance_category_delete'),
    path('transactions/', views.TransactionListView.as_view(), name='finance_transaction_list'),
    path('transactions/new/', views.TransactionCreateView.as_view(), name='finance_transaction_create'),
    path('transactions/<int:pk>/edit/', views.TransactionUpdateView.as_view(), name='finance_transaction_edit'),
    path('transactions/<int:pk>/delete/', views.TransactionDeleteView.as_view(), name='finance_transaction_delete'),
]
