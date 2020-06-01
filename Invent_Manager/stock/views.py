from django.shortcuts import render, redirect
from django.apps import apps
from django.views import generic
from django.contrib.auth import logout
from .models import *
from .forms import *

def home(request):
    loans = Loan.objects.all()
    customers = Customer.objects.all()
    total_customers = customers.count()
    total_loans = loans.count()
    returned = loans.filter(status='Returned').count()
    pending = loans.filter(status='Pending').count()

    context = {'loans':loans, 'customers':customers,
	'total_loans':total_loans, 'pending':pending, 'returned':returned

    }
    return render(request, 'stock/home.html', context)

def products(request):
    products = Product.objects.all()

    context = {'products': products}
    return render(request, 'stock/products.html', context)


def customer(request, pk):
	customer = Customer.objects.get(id=pk)

	loans = customer.loan_set.all()
	loan_count = loans.count()

	context = {'customer':customer, 'loans':loans, 'loan_count':loan_count}
	return render(request, 'stock/customer.html',context)



def LoanItemOut(request):
	form = LoanForm()
	if request.method == 'POST':
		# print('Printing POST:', request.POST)
		form = LoanForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'stock/loan_form.html', context)


def updateLoan(request, pk):

	loan = Loan.objects.get(id=pk)
	form = LoanForm(instance=loan)

	if request.method == 'POST':
		form = LoanForm(request.POST, instance=loan)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'stock/loan_form.html', context)


def deleteLoan(request, pk):
	loan = Loan.objects.get(id=pk)
	if request.method == "POST":
		loan.delete()
		return redirect('/')

	context = {'item':loan}
	return render(request, 'stock/delete.html', context)
