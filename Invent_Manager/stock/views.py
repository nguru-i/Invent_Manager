from django.shortcuts import render, redirect
from django.apps import apps
from django.views import generic
from django.contrib.auth import logout
from django.core.paginator import Paginator
from django.db.models import Sum, Count
from .models import *
from .forms import *
from .filters import *


def home(request):
    loans = Loan.objects.all()
    customers = Customer.objects.all()
    total_customers = customers.count()
    total_loans = loans.count()
    price = Loan.objects.select_related('product').filter(status='Out on loan').aggregate(sum=Sum('product__price'))
    out_on_loan_price = round(price.get('sum'), 2)
    out_on_loan = loans.filter(status='Out on loan').count()

    myFilter = LoanFilter(request.GET, queryset=loans)
    loans = myFilter.qs

    

    context = {'loans': loans, 'customers': customers,
               'total_loans': total_loans, 'out_on_loan': out_on_loan, 'out_on_loan_price': out_on_loan_price,
               'myFilter': myFilter
               }
    return render(request, 'stock/home.html', context)


def products(request):
    products = Product.objects.all()

    myFilter = ProductFilter(request.GET, queryset=products)
    products = myFilter.qs

    paginator = Paginator(products, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'products': products,
               'myFilter': myFilter, 'page_obj': page_obj}
    return render(request, 'stock/products.html', context)


def customer(request, pk):
    customer = Customer.objects.get(id=pk)

    loans = customer.loan_set.all()
    loan_count = loans.count()

    myFilter = LoanFilter(request.GET, queryset=loans)
    loans = myFilter.qs

    paginator = Paginator(loans, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'customer': customer, 'loans': loans, 'loan_count': loan_count,
               'myFilter': myFilter, 'page_obj': page_obj}
    return render(request, 'stock/customer.html', context)


def LoanItemOut(request, pk):
    customer = Customer.objects.get(id=pk)
    form = LoanForm(initial={'customer': customer})
    if request.method == 'POST':
        # print('Printing POST:', request.POST)
        form = LoanForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'stock/loan_form.html', context)


def updateLoan(request, pk):

    loan = Loan.objects.get(id=pk)
    form = LoanForm(instance=loan)

    if request.method == 'POST':
        form = LoanForm(request.POST, instance=loan)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'stock/loan_form.html', context)


def deleteLoan(request, pk):
    loan = Loan.objects.get(id=pk)
    if request.method == "POST":
        loan.delete()
        return redirect('/')

    context = {'item': loan}
    return render(request, 'stock/delete.html', context)
