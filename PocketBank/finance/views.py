from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Account, Transaction, TransactionCategory
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def FinanceHome(request):
    accounts = Account.objects.filter(owner=request.user)
    return render(request, 'finance/finance_home.html', {'accounts': accounts})

# ---------------- Accounts ----------------
class AccountListView(LoginRequiredMixin, ListView):
    model = Account
    template_name = 'finance/account_list.html'
    context_object_name = 'accounts'

    def get_queryset(self):
        return Account.objects.filter(owner=self.request.user)


class AccountCreateView(LoginRequiredMixin, CreateView):
    model = Account
    fields = ['name', 'balance', 'account_type']
    template_name = 'finance/account_form.html'
    success_url = reverse_lazy('finance_account_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class AccountUpdateView(LoginRequiredMixin, UpdateView):
    model = Account
    fields = ['name', 'balance', 'account_type']
    template_name = 'finance/account_form.html'
    success_url = reverse_lazy('finance_account_list')

    def get_queryset(self):
        return Account.objects.filter(owner=self.request.user)


class AccountDeleteView(LoginRequiredMixin, DeleteView):
    model = Account
    template_name = 'finance/account_confirm_delete.html'
    success_url = reverse_lazy('finance_account_list')

    def get_queryset(self):
        return Account.objects.filter(owner=self.request.user)


# ---------------- Categories ----------------
class CategoryListView(LoginRequiredMixin, ListView):
    model = TransactionCategory
    template_name = 'finance/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return TransactionCategory.objects.filter(user=self.request.user)


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = TransactionCategory
    fields = ['name', 'color']
    template_name = 'finance/category_form.html'
    success_url = reverse_lazy('finance_category_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = TransactionCategory
    fields = ['name', 'color']
    template_name = 'finance/category_form.html'
    success_url = reverse_lazy('finance_category_list')

    def get_queryset(self):
        return TransactionCategory.objects.filter(user=self.request.user)


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = TransactionCategory
    template_name = 'finance/category_confirm_delete.html'
    success_url = reverse_lazy('finance_category_list')

    def get_queryset(self):
        return TransactionCategory.objects.filter(user=self.request.user)


# ---------------- Transactions ----------------
class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'finance/transaction_list.html'
    context_object_name = 'transactions'

    def get_queryset(self):
        account_id = self.kwargs.get("pk")
        return Transaction.objects.filter(account__owner=self.request.user, account_id=account_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['account'] = Account.objects.get(pk=self.kwargs['pk'], owner=self.request.user)
        return context


class TransactionCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    fields = ['account', 'amount', 'category', 'description', 'date', 'transaction_type']
    template_name = 'finance/transaction_form.html'

    def get_success_url(self):
        return reverse_lazy('finance_transaction_list', kwargs={'pk': self.object.account.pk})

    def get_queryset(self):
        return Transaction.objects.filter(account__owner=self.request.user)


class TransactionUpdateView(LoginRequiredMixin, UpdateView):
    model = Transaction
    fields = ['account', 'amount', 'category', 'description', 'date', 'transaction_type']
    template_name = 'finance/transaction_form.html'

    def get_success_url(self):
        return reverse_lazy('finance_transaction_list', kwargs={'pk': self.object.account.pk})

    def get_queryset(self):
        return Transaction.objects.filter(account__owner=self.request.user)


class TransactionDeleteView(LoginRequiredMixin, DeleteView):
    model = Transaction
    template_name = 'finance/transaction_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('finance_transaction_list', kwargs={'pk': self.object.account.pk})

    def get_queryset(self):
        return Transaction.objects.filter(account__owner=self.request.user)
