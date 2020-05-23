from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='stock-home'),
    path('about/', views.about, name='stock-about'),
]
