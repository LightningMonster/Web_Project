from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Redirect to the home page or any other desired page upon successful login
            return redirect('home')

    return render(request, 'login.html')

def home(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

def contact(request):
    return render(request, 'contactpage.html')

def signup(request):
        if request.method == "POST":
            firstName = request.POST['firstName']
            lastName = request.POST['lastName']
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            confirmPassword = request.POST['confirmPassword']
        
            myuser = User.objects.create_user(username, email, password)
            myuser.first_name = firstName
            myuser.last_name = lastName
            myuser.save()
            messages.success(request, "Account created successfully!")
            return render(request, 'index.html')

        return render(request, 'signup.html')
        
