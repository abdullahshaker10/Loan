from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, ListView, View
from .models import Loan, Offer
from .forms import LoanCreateForm, OfferCreateForm
from django.shortcuts import render, redirect
from django.urls import reverse
from rest_framework.generics import UpdateAPIView, RetrieveUpdateAPIView
from .serializers import *
import json
from rest_framework.response import Response
import datetime
from datetime import date
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib import messages


class Home(TemplateView):
    template_name = "main.html"


class LoanCreate(LoginRequiredMixin, View):
    form_class = LoanCreateForm
    template_name = 'loan/create_loan.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            "form": self.form_class
        })

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            loan = form.save(commit=False)
            current_user = request.user
            loan.borrower = current_user
            loan.save()
        return redirect(reverse("home"))


class CheckBalanceMixin(object):
    model = Offer
    lookup = 'pk'

    def check_balance(self, request, *args, **kwargs):
        loan_id = self.kwargs.get(self.lookup)
        loan_amount = Loan.objects.get(id=loan_id).amount
        user_balance = self.request.user.profile.balance
        if user_balance < loan_amount:
            messages.error(
                request, "you don't have enough balance")
            return False
        return True

class OfferCreate(LoginRequiredMixin, CheckBalanceMixin, View):
    model = Offer
    form_class = OfferCreateForm
    template_name = 'loan/create_offer.html'

    def get_context_data(self, *args, **kwargs):
        context = super(MyView, self).get_context_data(*args, **kwargs)
        context['messages'] = messages
        return context

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            "form": self.form_class
        })

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            if self.check_balance(self.request):
                offer = form.save(commit=False)
                current_user = request.user
                loan_id = self.kwargs['pk']
                loan = Loan.objects.get(id=loan_id)
                offer.loan = loan
                offer.investor = current_user
                offer.save()
        return redirect(reverse("home"))


class LoansList(ListView):
    queryset = Loan.objects.all()
    template_name = 'loan/loan_list.html'
    context_object_name = 'loans'


class offersList(ListView):
    template_name = 'loan/offer_list.html'
    context_object_name = 'offers'

    def get_queryset(self, **kwargs):
        current_user = self.request.user
        loans = Loan.objects.filter(borrower=current_user).all()
        queryset = Offer.objects.filter(loan__in=loans)

        return queryset


class OfferApi(RetrieveUpdateAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    lookup_field = 'pk'
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        body = json.loads(request.body)
        if body['state'] == "Funded":
            instance.rest_paymrnts = instance.loan.period
            profile = instance.investor.profile
            profile.balance = profile.balance - instance.loan.amount
            profile.save()
        if body['state'] == "Paying":
            instance.rest_paymrnts = instance.rest_paymrnts - 1
        instance.state = body['state']
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class LoanApi(RetrieveUpdateAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    lookup_field = 'pk'
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        body = json.loads(request.body)
        instance.state = body['state']

        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
