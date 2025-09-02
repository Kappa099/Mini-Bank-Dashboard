from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Account(models.Model):
    name = models.CharField(max_length=50)
    balance = models.DecimalField(max_digits=15, decimal_places=2)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    ACCOUNT_TYPES = [
    ('checking', 'Checking'),
    ('savings', 'Savings'),
    ('credit', 'Credit Card'),
]
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES)

    def __str__(self):
        return f"{self.name}"

class TransactionCategory(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=7, default='#000000')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    category = models.ForeignKey(TransactionCategory, on_delete=models.CASCADE)
    description = models.CharField(max_length=300, blank=True)
    date = models.DateField(default=timezone.now)

    TRANSACTION_TYPE = [
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
    ]
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE)

    def __str__(self):
        return f"{self.transaction_type} - ${self.amount} ({self.account.name})"