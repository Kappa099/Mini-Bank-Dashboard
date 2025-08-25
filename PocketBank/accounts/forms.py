from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from .models import Account
from django.urls import reverse_lazy

class AccountCreateView(CreateView):
    model = Account
    fields = ['name', 'balance', 'account_type']  # whatever fields your model has
    template_name = 'accounts/account_form.html'
    success_url = reverse_lazy('accounts_list')


class AccountUpdateView(UpdateView):
    model = Account
    fields = ['name', 'balance', 'account_type']
    template_name = 'accounts/account_form.html'
    success_url = reverse_lazy('accounts_list')


class AccountDeleteView(DeleteView):
    model = Account
    template_name = 'accounts/account_confirm_delete.html'
    success_url = reverse_lazy('accounts_list')


