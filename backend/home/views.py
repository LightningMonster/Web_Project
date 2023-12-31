from django.shortcuts import render,HttpResponse

def home(request):
    return render(request, 'index.html')
    
# Create your views here.
