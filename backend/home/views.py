from django.shortcuts import render,HttpResponse

def home(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

def contact(request):
    return render(request, 'contactpage.html')
    
# Create your views here.
