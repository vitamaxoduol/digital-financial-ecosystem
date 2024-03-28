from django.urls import path
from . import views
from django.db.models import Sum

urlpatterns = [
    path('account/', views.user_account, name='user_account'),
    path('account/add/', views.AccountCreateView.as_view(), name='account_create'),
    path('account/activity/str:account_number>/', views.TransactionListView.as_view(), name='transaction_list'),
]