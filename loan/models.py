from django.db import models
from django.contrib.auth.models import User


class Loan(models.Model):
    borrower = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name='loan', null=True, blank=True)
    amount = models.FloatField(default=0)
    period = models.IntegerField()
    reason = models.TextField()
    state = models.CharField(max_length=50, default="Active")


class Offer(models.Model):
    investor = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="offer", null=True, blank=True)
    loan = models.ForeignKey(
        Loan, on_delete=models.SET_NULL, related_name="offer",  null=True, blank=True)
    interest_rate = models.FloatField( default=0)
    state = models.CharField(max_length=50, default="Pending")
    rest_paymrnts = models.IntegerField(default=0)

    @property
    def annual_amount_with_rate(self):
        added_amount = (self.interest_rate / 100) * self.loan.amount
        return added_amount + self.loan.amount

    @property
    def monthly_amount_with_rate(self):
        annual_amount = self.annual_amount_with_rate
        monthly_amount = annual_amount / self.loan.period
        return monthly_amount
    @property
    def site_commission(self):
        return 3

    @property
    def final_amount(self):
        total = (self.monthly_amount_with_rate *
                 self.loan.period) + self.site_commission
        return total
