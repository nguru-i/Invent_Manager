from django.shortcuts import render, redirect
from django.contrib import messages
from django import forms
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm
from django.contrib.auth.models import Group
from django.apps import apps
from django.contrib.auth import authenticate, login, logout
from django.views import generic
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.core.paginator import Paginator
from django.db.models import Sum, Count, F
from .models import *
from .forms import *
from .filters import *
from.decorators import *
import datetime


@unauthenticated_user
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email =  form.cleaned_data.get('email')
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            Customer.objects.create(user=user,
            	name=f'{user.first_name}  {user.last_name}',
                email = email
            	)
            messages.success(
                request, f'{username}, your account has been created. You can now use it to log in.')
            return redirect('login')
        else:
            messages.error(request, form.errors)
    else:
        form = UserRegistrationForm()
    return render(request, 'stock/register.html', {'form': form})


@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('stock-home')
        else:
            messages.error(request, 'Please enter correct credentials')

    context = {}
    return render(request, 'stock/login.html', context)


@login_required
def logoutPage(request):
	logout(request)
	return redirect('login')


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    loans = request.user.customer.loan_set.all().order_by('due_back')

    total_loans = loans.count()
    out_on_loan = loans.filter(status='Out on loan').count()
    
    out_on_loan_items = loans.filter(status='Out on loan').order_by('due_back')
    price = 0
    for out_on_loan_item in out_on_loan_items:
        price += out_on_loan_item.product.price
    out_on_loan_price = price

    paginator = Paginator(loans, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # dateDue = loans.loan.due_back - timezone.now() - datetime.timedelta(days=1)


    context = {'out_on_loan': out_on_loan, 'total_loans': total_loans, 'page_obj': page_obj, 
    'out_on_loan_price': out_on_loan_price, }
    return render(request, 'stock/user.html', context)



@login_required(login_url='login')
@admin_only
def home(request):
    loans = Loan.objects.all().order_by('due_back')
    total_loans = loans.count()
    

    out_on_loan_items = loans.filter(status='Out on loan')  
    price = 0
    for out_on_loan_item in out_on_loan_items:
        price += out_on_loan_item.product.price
    out_on_loan_price = price


    out_on_loan = loans.filter(status='Out on loan').count()

    myFilter = LoanFilter(request.GET, queryset=loans)
    loans = myFilter.qs

    customers = Customer.objects.all().order_by('id')
    myCustFilter = CustomerFilter(request.GET, queryset=customers)
    customers = myCustFilter.qs
    

    context = {'loans': loans, 'customers': customers,
               'total_loans': total_loans, 'out_on_loan': out_on_loan, 'out_on_loan_price': out_on_loan_price,
               'myFilter': myFilter, 'myCustFilter': myCustFilter
               }
    return render(request, 'stock/home.html', context)


@login_required(login_url='login')
@admin_only
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


# @login_required(login_url='login')
# @admin_only
# def stocks(request):
#     stocks = Stock.objects.all()

#     myFilter = StockFilter(request.GET, queryset=stocks)
#     stocks = myFilter.qs

#     paginator = Paginator(stocks, 10)

#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     context = {'stocks': stocks,
#                'myFilter': myFilter, 'page_obj': page_obj}
#     return render(request, 'stock/stocks.html', context)


@login_required(login_url='login')
@admin_only
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


@login_required(login_url='login')
@admin_only
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


@login_required(login_url='login')
@admin_only
def updateCustomer(request, pk):

    customer = Customer.objects.get(id=pk)
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer', pk)

    context = {'form': form}
    return render(request, 'stock/customer_form.html', context)


@login_required(login_url='login')
@admin_only
def updateLoan(request, pk):

    loan = Loan.objects.get(id=pk)
    form = LoanForm(instance=loan)
    form.fields['customer'].disabled = True
    form.fields['due_back'].widget = forms.SelectDateWidget()
    if request.method == 'POST':
        form = LoanForm(request.POST, instance=loan)
        form.fields['customer'].disabled = True
        form.fields['due_back'].widget = forms.SelectDateWidget()
        if form.is_valid():
            if form.has_changed():

                # product = Product.objects.filter(id=pk).select_related('product')
                # product = Loan.objects.select_related('product').filter(id=pk)
                # item = Loan.objects.get(id=pk)
                q1 = Loan.objects.filter(id=pk).select_related('product')
                # print(produc.product.quantity)
                item = q1.get()
                
                # productq = product.get(name=product)
                # productq = Product.objects.get(quantity__product=quantity)
                # print(productq)
                
                if form.cleaned_data['status'] =='Returned':
                    print(f'inside the if')
                    item.product.quantity  += 1
                    print(f'inner if')
                else:item.product.quantity  -= 1
                temp = item.product.quantity
                print(temp, item.product.description)
                print(f'end of outter if')
                prodForm = ProductForm(request.POST,instance=item.product)
                # prod = prodForm.save(commit=False)
                print('__________')
                # print(prodForm.cleaned_data)
                prodForm.quantity = temp
                if prodForm.is_valid():
                    # prodForm.quantity = temp
                    # print(prodForm.cleaned_data)
                    print(prodForm)
                    prodForm.save()
                    print('__________')




            print(item.product.quantity)

            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'stock/loan_form.html', context)


@login_required(login_url='login')
@admin_only
def deleteLoan(request, pk):
    loan = Loan.objects.get(id=pk)
    if request.method == "POST":
        loan.delete()
        return redirect('/')

    context = {'item': loan}
    return render(request, 'stock/delete.html', context)


