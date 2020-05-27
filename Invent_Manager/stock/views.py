from django.shortcuts import render
from django.contrib.auth import logout



def home(request):
    return render(request, 'stock/home.html', {'title': 'Home'})


def about(request):
    return render(request, 'stock/about.html', {'title': 'About'})