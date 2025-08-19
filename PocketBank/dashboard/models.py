from django.db import models
from django.contrib.auth.models import User

class DashboardSummary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_balance = models.DecimalField(max_digits=15, decimal_places=2)
    total_income = models.DecimalField(max_digits=15, decimal_places=2)
    total_expense = models.DecimalField(max_digits=15, decimal_places=2)
    last_updated = models.DateTimeField(auto_now=True)
