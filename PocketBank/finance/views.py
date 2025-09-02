from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Account, Transaction, TransactionCategory
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render, get_object_or_404



@login_required
def FinanceHome(request):
    accounts = Account.objects.filter(owner=request.user)
    return render(request, 'finance/finance_home.html', {'accounts': accounts})

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


class AccountDetailView(LoginRequiredMixin, DetailView):
    model = Account
    template_name = 'finance/account_detail.html'
    context_object_name = 'account'

    def get_queryset(self):
        return Account.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        account = self.object

        context['transactions'] = Transaction.objects.filter(account=account)

        context['total_income'] = context['transactions'].filter(transaction_type='deposit').aggregate(Sum('amount'))['amount__sum'] or 0
        context['total_expense'] = context['transactions'].filter(transaction_type='withdrawal').aggregate(Sum('amount'))['amount__sum'] or 0

        return context

class AccountDeleteView(LoginRequiredMixin, DeleteView):
    model = Account
    template_name = 'finance/account_confirm_delete.html'
    success_url = reverse_lazy('finance_account_list')

    def get_queryset(self):
        return Account.objects.filter(owner=self.request.user)


class CategoryListView(LoginRequiredMixin, ListView):
    model = TransactionCategory
    template_name = 'finance/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return TransactionCategory.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for category in context['categories']:
            category.total_income = Transaction.objects.filter(
                category=category,
                transaction_type='deposit'
            ).aggregate(Sum('amount'))['amount__sum'] or 0

            category.total_expense = Transaction.objects.filter(
                category=category,
                transaction_type='withdrawal'
            ).aggregate(Sum('amount'))['amount__sum'] or 0
        return context

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


from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

class TransactionCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    fields = ['account', 'amount', 'category', 'description', 'date', 'transaction_type']
    template_name = 'finance/transaction_form.html'

    def get_initial(self):
        initial = super().get_initial()
        account_id = self.request.GET.get('account')
        if account_id:
            initial['account'] = get_object_or_404(Account, pk=account_id, owner=self.request.user)
        return initial

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['account'].queryset = Account.objects.filter(owner=self.request.user)
        form.fields['category'].queryset = TransactionCategory.objects.filter(user=self.request.user)
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        account_id = self.request.GET.get('account')
        if account_id:
            context['account'] = get_object_or_404(Account, pk=account_id, owner=self.request.user)
        return context

    def get_success_url(self):
        return reverse_lazy('finance_transaction_list', kwargs={'pk': self.object.account.pk})

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
