from django import forms

from .models import *


class LoanCreateForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ['amount', 'period', 'reason']


class OfferCreateForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ['interest_rate', ]



