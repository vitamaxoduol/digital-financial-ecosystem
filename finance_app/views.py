from django.shortcuts import render
from .models import UserProfile
from django.db.models import Sum
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.views.generic import ListView
from django.urls import reverse_lazy
from .models import Account
from .models import Transaction
from django.db.models import Q
def user_account(request):
    user = request.user

    # Retrieve the user's account information
    try:
        user_profile = user.userprofile
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=user)

    # Retrieve the user's account balance
    balance = user_profile.account_set.aggregate(total=Sum('balance'))['total'] or 0

    # Retrieve the user's transaction history
    transactions = user_profile.transaction_set.all().order_by('-timestamp')

    return render(request, 'user_account.html', {
        'user': user,
        'user_profile': user_profile,
        'balance': balance,
        'transactions': transactions,                                                                                   
    })




class AccountCreateView(LoginRequiredMixin, CreateView):
    model = Account
    fields = ['account_number', 'balance', 'currency']
    template_name = 'account/create.html'

    def form_valid(self, form):
        form.instance.user_profile = self.request.user.userprofile
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('user_account')
    

class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'account/transaction_list.html'

    def get_queryset(self):
        user = self.request.user
        user_profile = user.userprofile
        account_number = self.kwargs.get('account_number')

        if account_number:
            return user_profile.transaction_set.filter(account_number=account_number)

        return user_profile.transaction_set.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['account_number'] = self.kwargs.get('account_number')
        return context
    

class TransactionHistoryListView(LoginRequiredMixin, ListView):
    model = Transaction
    context_object_name = 'transactions'
    template_name = 'finance_app/transaction_history.html'
    paginate_by = 10  # Number of transactions per page

    def get_queryset(self):
        qs = Transaction.objects.filter(
            Q(user_profile__user=self.request.user) &
            Q(transaction_type__in=['deposit', 'withdrawal', 'transfer'])
        )

        # Filter transactions by date
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        if start_date and end_date:
            qs = qs.filter(timestamp__range=[start_date, end_date])

        # Filter transactions by account
        account_number = self.request.GET.get('account_number')
        if account_number:
            qs = qs.filter(account_number=account_number)

        # Filter transactions by transaction type
        transaction_type = self.request.GET.get('transaction_type')
        if transaction_type:
            qs = qs.filter(transaction_type=transaction_type)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add start_date, end_date, account_number, and transaction_type to context
        context['start_date'] = self.request.GET.get('start_date')
        context['end_date'] = self.request.GET.get('end_date')
        context['account_number'] = self.request.GET.get('account_number')
        context['transaction_type'] = self.request.GET.get('transaction_type')

        return context


