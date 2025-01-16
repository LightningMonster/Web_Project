# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.models import StockData
from decimal import Decimal
from django.db.models import Max, F
from django.db.models import Subquery, OuterRef
from django.core.paginator import Paginator

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
    # Define the stock symbols you're interested in
    stock_symbols = ['SHILPAMED.BO', 'LAURUSLABS.NS', 'INFOSYS', 'ADANI', 'LT']

    # Fetch the latest date for each stock symbol
    latest_dates = StockData.objects.filter(
        stock_symbol__in=stock_symbols
    ).values('stock_symbol').annotate(latest_date=Max('date'))

    # Prepare a list to hold the latest stock data for each stock symbol
    stock_data = []

    # Fetch the latest stock entry for each symbol
    for latest in latest_dates:
        # Fetch the stock entry for the latest date of the stock_symbol
        stock = StockData.objects.filter(
            stock_symbol=latest['stock_symbol'],
            date=latest['latest_date']
        ).first()  # We only need the latest entry

        if stock:
            # Calculate the percentage change
            change = ((stock.close - stock.open) / stock.open) * 100 if stock.open else 0
            stock_data.append({
                'symbol': stock.stock_symbol,
                'last_price': stock.close,
                'change': round(change, 2)
            })

    return render(request, 'pages/home2.html', {'stock_data': stock_data})


def home1(request):
    # Fetch the latest 20 unique stocks by date
    stocks = (
        StockData.objects.order_by('stock_symbol', '-date')
        .distinct('stock_symbol')[:20]
    )

    stock_data = []
    for stock in stocks:
        # Fetch the previous day's data for the same stock symbol
        prev_day = (
            StockData.objects.filter(
                stock_symbol=stock.stock_symbol, date__lt=stock.date
            )
            .order_by('-date')
            .first()
        )

        # Calculate price change
        if prev_day:
            price_change = ((stock.close - prev_day.close) / prev_day.close) * Decimal(100)
        else:
            price_change = Decimal(0)

        stock_data.append({
            'symbol': stock.stock_symbol,
            'last_price': stock.close,
            'price_change': price_change,
        })

    return render(request, 'pages/home1.html', {'stock_data': stock_data})

def calculators(request):
    return render(request, 'pages/calculator.html')

from django.db.models import Max, Subquery, OuterRef, F

def nse_stocks(request):
    # Get the most recent entry for each stock symbol ending with '.BS'
    stocks = StockData.objects.filter(stock_symbol__endswith='.BS').values('stock_symbol').annotate(latest_date=Max('date'))

    # Get the last price for each stock based on the latest date
    stock_info = []
    
    for stock in stocks:
        latest_stock = StockData.objects.filter(
            stock_symbol=stock['stock_symbol'], 
            date=stock['latest_date']
        ).first()
        
        # Calculate price change (for simplicity, assume previous price is from the last entry)
        previous_stock = StockData.objects.filter(
            stock_symbol=stock['stock_symbol']
        ).exclude(date=stock['latest_date']).order_by('-date').first()

        if previous_stock:
            price_change = latest_stock.close - previous_stock.close
            price_change_percent = (price_change / previous_stock.close) * 100 if previous_stock.close != 0 else 0
        else:
            price_change = 0
            price_change_percent = 0
        
        stock_info.append({
            'symbol': latest_stock.stock_symbol,
            'last_price': latest_stock.close,
            'price_change': price_change,
            'price_change_percent': price_change_percent,
        })
    
    return render(request, 'pages/nse_stocks.html', {'stock_info': stock_info})

def bse_stocks(request):
    # Get the most recent entry for each stock symbol ending with '.BS'
    stocks = StockData.objects.filter(stock_symbol__endswith='.BS').values('stock_symbol').annotate(latest_date=Max('date'))

    # Get the last price for each stock based on the latest date
    stock_info = []
    
    for stock in stocks:
        latest_stock = StockData.objects.filter(
            stock_symbol=stock['stock_symbol'], 
            date=stock['latest_date']
        ).first()
        
        # Calculate price change (for simplicity, assume previous price is from the last entry)
        previous_stock = StockData.objects.filter(
            stock_symbol=stock['stock_symbol']
        ).exclude(date=stock['latest_date']).order_by('-date').first()

        if previous_stock:
            price_change = latest_stock.close - previous_stock.close
            price_change_percent = (price_change / previous_stock.close) * 100 if previous_stock.close != 0 else 0
        else:
            price_change = 0
            price_change_percent = 0
        
        stock_info.append({
            'symbol': latest_stock.stock_symbol,
            'last_price': latest_stock.close,
            'price_change': price_change,
            'price_change_percent': price_change_percent,
        })
    
    return render(request, 'pages/bse_stocks.html', {'stock_info': stock_info})

def dashboard(request):
    """
    View function for the user dashboard.
    """
    # Add any context data you want to pass to the template
    context = {
        'username': request.user.username,  # Example: Pass the username to the template
    }
    return render(request, 'pages/dashboard.html', context)