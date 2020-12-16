
from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.Home.as_view(), name="home"),
    path('loan/create', views.LoanCreate.as_view(), name="loan-create"),
    path('offer/create/<int:pk>', views.OfferCreate.as_view(), name="offer-create"),
    path('loans/', views.LoansList.as_view(), name="loans-list"),
    path('offers/', views.offersList.as_view(), name="offers-list"),
    path('api/offer/<int:pk>', views.OfferApi.as_view(), name="update-offer"),
    path('api/loan/<int:pk>', views.LoanApi.as_view(), name="update-loan"),

]
