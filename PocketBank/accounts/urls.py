from django.urls import path
from .views import AccountListView, AccountCreateView, AccountUpdateView, AccountDeleteView, ProfileDetailView, ProfileUpdateView
from accounts.views import RegisterView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', AccountListView.as_view(), name='accounts_list'),         
    path('new/', AccountCreateView.as_view(), name='account_create'),  
    path('<int:pk>/edit/', AccountUpdateView.as_view(), name='account_edit'),
    path('<int:pk>/delete/', AccountDeleteView.as_view(), name='account_delete'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileDetailView.as_view(), name='profile_detail'),
    path('profile/edit/', ProfileUpdateView.as_view(), name='profile_edit'),
]
