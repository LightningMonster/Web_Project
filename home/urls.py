from django.contrib import admin
from django.urls import path,include
from home import views
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('contact/', views.contact, name='contact'),
]