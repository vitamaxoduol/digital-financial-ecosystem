from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
# from django.utils.translation import gettext_lazy as _

User = get_user_model()

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Additional fields for user information
    account_number = models.CharField(max_length=20)
    # ...

    def __str__(self):
        return self.user.username
    

def create_user(username, email, password, first_name, last_name, phone_number, **extra_fields):
    user = User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name, **extra_fields)
    user.phone_number = phone_number
    user.save()

    user_profile = UserProfile.objects.create(user=user, **extra_fields)
    user_profile.save()

    return user

def create_superuser(username, email, password, **extra_fields):
    user = User.objects.create_superuser(username, email, password, **extra_fields)
    # Create and save a user profile
    user_profile = UserProfile(user=user, **extra_fields)
    user_profile.save()
    return user


class Account(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=20)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, default='USD')

class Transaction(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=20, choices=(
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
        ('transfer', 'Transfer')
    ))
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Savings(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=20)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    maturity_date = models.DateField()

class Loan(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=20)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    repayment_schedule = models.TextField()
    loan_type = models.CharField(max_length=20, choices=(
        ('personal', 'Personal'),
        ('business', 'Business')
    ))

class SMSLog(models.Model):
    id = models.AutoField(primary_key=True)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    recipient_number = models.CharField(max_length=20)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20)

class SMSCommand(models.Model):
    id = models.AutoField(primary_key=True)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    command = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20)



class Savings(models.Model):
    user_profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    goal = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Calculate savings progress and save

        if self.goal:
            self.progress = (self.balance / self.goal) * 100
        else:
            self.progress = 0

        super().save(*args, **kwargs)
