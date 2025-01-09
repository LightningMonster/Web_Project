# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.models import StockData

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already registered')
            else:
                user = User.objects.create_user(
                    username=username,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    email=email
                )
                user.save()
                messages.success(request, 'Registration successful. Please login.')
                return redirect('login')
        else:
            messages.error(request, 'Passwords do not match')
    return render(request, 'accounts/register.html')

def login_user(request):
    if request.method == 'POST':
        email = request.POST['email']  # Get email from form
        password = request.POST['password']  # Get password from form

        # Get the username associated with the email
        try:
            user = User.objects.get(email=email)  # Check if email exists
            username = user.username  # Retrieve the username
        except User.DoesNotExist:
            messages.error(request, 'Invalid email or password')
            return render(request, 'accounts/login.html')

        # Authenticate using the retrieved username and provided password
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful')
            return redirect('home2')  # Redirect to Home 2 page
        else:
            messages.error(request, 'Invalid email or password')

    return render(request, 'accounts/login.html')

def logout_user(request):
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('/')

@login_required
def home2(request):
    return render(request, 'pages/home2.html')


def home1(request):
    # Fetch the last 5 entries for each of the 5 stock symbols
    stock_symbols = StockData.objects.values_list('stock_symbol', flat=True).distinct()[:5]
    stock_data = {}
    for symbol in stock_symbols:
        stock_data[symbol] = StockData.objects.filter(stock_symbol=symbol).order_by('-date')[:5]
    
    context = {
        'stock_data': stock_data,
    }
    return render(request, 'pages/home1.html', context)