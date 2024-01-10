from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        login_type = request.POST.get('login_type')  
        identifier = request.POST.get('identifier')
        password = request.POST.get('password')

        # Validate login type and authenticate
        user = None
        if login_type == 'email':
            user = authenticate(request, email=identifier, password=password)
        elif login_type == 'username':
            user = authenticate(request, username=identifier, password=password)

        if user is not None:
            login(request, user)  
            messages.success(request, 'Successfully logged in!')
            
            return redirect('home')  
        else:
            # Authentication failed
            messages.error(request, 'Invalid credentials. Please try again.')

    return render(request, 'Login_Page.html')

def index(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'Login_Page.html')

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

            # passwords should match
            if password != confirmPassword:
                 messages.error(request, "Password do not match.")
                 return render(request, 'signup.html')
        
            myuser = User.objects.create_user(username, email, password)
            myuser.first_name = firstName
            myuser.last_name = lastName
            myuser.save()
            messages.success(request, "Account created successfully!")
            return render(request, 'index.html')

        return render(request, 'signup.html')
        
