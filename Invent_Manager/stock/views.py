from django.shortcuts import render
from django.apps import apps
from django.views import generic
from django.contrib.auth import logout
from .models import *
from .forms import *



def home(request):
    # model_list = apps.get_app_config('stock').get_models()
    model_list = apps.all_models['stock']
    context = {'model_list':model_list}
    return render(request, 'stock/home.html', context)


def detail(request):
    form = ChassisForm()
    context = {'form':form}
    return render(request, 'stock/detail.html', context)


class IndexView(generic.ListView):
    template_name = 'stock/home.html'