from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='stock-home'),
    path('detail/', views.detail, name='stock-detail'),
]
