from django.contrib import admin
from django.urls import path
from .views import DashboardHome, AccountDetails, TransactionDetails, CategoryReport, MonthlySummary

urlpatterns = [
    path('', DashboardHome.as_view(), name='dashboard_home'),
    path('account/<int:pk>', AccountDetails.as_view(), name='account_details'),
    path('transaction/<int:pk>', TransactionDetails.as_view(), name='transaction_details'),
    path('categories/', CategoryReport.as_view(), name='categories'),
    path('summery/', MonthlySummary.as_view(), name='summery')
]