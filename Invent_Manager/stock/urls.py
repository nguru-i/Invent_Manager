from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.register, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutPage, name="logout"),

    path('', views.home, name='stock-home'),
    path('user/', views.userPage, name="user-page"),
    path('products/', views.products, name='stock-products'),
    path('customer/<str:pk>/', views.customer, name="customer"),

    path('create_loan/<str:pk>/', views.LoanItemOut, name="create_loan"),
    path('update_loan/<str:pk>/', views.updateLoan, name="update_loan"),
    path('delete_loan/<str:pk>/', views.deleteLoan, name="delete_loan"),
]
