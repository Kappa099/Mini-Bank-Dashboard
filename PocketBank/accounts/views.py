from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from finance.models import Account  


class AccountListView(LoginRequiredMixin, ListView):
    model = Account
    template_name = 'accounts/accounts_list.html'
    context_object_name = 'accounts' 

    def get_queryset(self):
        return Account.objects.filter(owner=self.request.user)

class AccountCreateView(LoginRequiredMixin, CreateView):
    model = Account
    template_name = 'accounts/account_form.html'
    fields = ['name', 'balance', 'account_type']  
    success_url = reverse_lazy('accounts_list')


    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class AccountUpdateView(LoginRequiredMixin, UpdateView):
    model = Account
    template_name = 'accounts/account_form.html'
    fields = ['name', 'balance', 'account_type']
    success_url = reverse_lazy('accounts_list')

    def get_queryset(self):
        return Account.objects.filter(owner=self.request.user)

class AccountDeleteView(LoginRequiredMixin, DeleteView):
    model = Account
    template_name = 'accounts/account_confirm_delete.html'
    success_url = reverse_lazy('accounts_list')

    def get_queryset(self):
        return Account.objects.filter(owner=self.request.user)
