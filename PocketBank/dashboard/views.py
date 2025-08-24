from django.shortcuts import render
from django.views.generic import ListView, DetailView
from accounts.models import UserProfile
from finance.models import Account, Transaction, TransactionCategory
from django.db.models import Sum
from django.contrib.auth.mixins import LoginRequiredMixin

class DashboardHome(LoginRequiredMixin, ListView):
    model = Account
    template_name = '/dashboard/dashboard_home.html'
    context_object_name = 'accounts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        transactions = Transaction.objects.filter(account__owner = self.request.user)
        context["total_income"] = transactions.filter(transaction_type="deposit").aggregate(models.Sum("amount"))["amount__sum"] or 0
        context["total_expense"] = transactions.filter(transaction_type="withdrawal").aggregate(models.Sum("amount"))["amount__sum"] or 0
        return context
    
class AccountDetails(DetailView):
    model = Account
    template_name = '/dashboard/account_details.html'
    context_object_name = 'account'

    def get_queryset(self):
        return Account.objects.filter(owner=self.request.user)
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["transactions"] = Transaction.objects.filter(account=self.object)
        return context
class TransactionDetails(DetailView):
    model = Transaction
    template_name = '/dashboard/transaction_details.html'
    context_object_name = 'transaction'

    def get_queryset(self):
        return Transaction.objects.filter(account__owner=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["related_transactions"] = Transaction.objects.filter(account=self.object.account).exclude(pk=self.object.pk)
        return context
    
class CategoryReport(ListView):
    model = TransactionCategory
    template_name = '/dashboard/transaction_category.html'
    context_object_name = 'categories' 

    def get_queryset(self):
        return TransactionCategory.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for category in context['categories']:
            category.total_income = Transaction.objects.filter(
                category=category, transaction_type='deposit'
            ).aggregate(Sum('amount'))['amount__sum'] or 0
            category.total_expense = Transaction.objects.filter(
                category=category, transaction_type='withdrawal'
            ).aggregate(Sum('amount'))['amount__sum'] or 0
        return context

class MonthlySummary(ListView):
    model = Transaction
    template_name = '/dashboard/monthly_summary.html'
    context_object_name = 'monthly_data'

    def get_queryset(self):
        return Transaction.objects.filter(account__owner=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        transactions = self.get_queryset()
        monthly_data = {}

        for t in transactions:
            month = t.date.strftime("%Y-%m") 
            if month not in monthly_data:
                monthly_data[month] = {'income': 0, 'expense': 0}
            if t.transaction_type == 'deposit':
                monthly_data[month]['income'] += t.amount
            else:
                monthly_data[month]['expense'] += t.amount

        context['monthly_data'] = monthly_data
        return context
