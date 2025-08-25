from django.urls import path
from .views import AccountListView, AccountCreateView, AccountUpdateView, AccountDeleteView

urlpatterns = [
    path('', AccountListView.as_view(), name='accounts_list'),         
    path('new/', AccountCreateView.as_view(), name='account_create'),    
    path('<int:pk>/edit/', AccountUpdateView.as_view(), name='account_edit'),  
    path('<int:pk>/delete/', AccountDeleteView.as_view(), name='account_delete'),  
]
