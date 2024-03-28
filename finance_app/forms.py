from django import forms
from .models import Savings
from django.utils.translation import gettext_lazy as _


class SavingsForm(forms.ModelForm):
    class Meta:
        model = Savings
        fields = ['name', 'balance', 'goal']
        labels = {
            'name': _('Name'),
            'balance': _('Balance'),
            'goal': _('Goal'),
        }
        help_texts = {
            'name': _('Enter the name of the savings.'),
            'balance': _('Enter the current balance of the savings.'),
            'goal': _('Enter the goal amount of the savings.'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Calculate savings progress and save

        if self.instance.goal:
            self.instance.progress = (self.instance.balance / self.instance.goal) * 100
        else:
            self.instance.progress = 0