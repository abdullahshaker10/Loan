from rest_framework import serializers
from .models import *


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = '__all__'


class OfferSerializer(serializers.ModelSerializer):
    loan = LoanSerializer(required=True)

    class Meta:
        model = Offer
        fields = '__all__'
