"""Invent_Manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('stock.urls')),
    path('/admin/report_builder/', include('report_builder.urls')),

]


# design similar applications 

# background reseearch : waht are web applications. why 

# requirement and design chapter
# req: func and non
# design. before talking about my design, talk about other existing designs
