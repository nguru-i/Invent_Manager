from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='stock-home'),
    path('products/', views.products, name='stock-products'),
    path('customer/<str:pk>/', views.customer, name="customer"),

    path('create_loan/', views.LoanItemOut, name="create_loan"),
    path('update_loan/<str:pk>/', views.updateLoan, name="update_loan"),
    path('delete_loan/<str:pk>/', views.deleteLoan, name="delete_loan"),
]
