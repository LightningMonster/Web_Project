from django.contrib import admin
from django.urls import path,include
from home import views
from .views import login_view

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', login_view, name='login'),
    path('contact/', views.contact, name='home'),
]