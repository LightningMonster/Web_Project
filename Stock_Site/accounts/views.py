# accounts/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.models import StockData
from decimal import Decimal
from django.db.models import Subquery, OuterRef
from django.core.paginator import Paginator
from django.db.models import Max, Min
from .models import StockData, Watchlist
import feedparser
from urllib.parse import quote 

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

@login_required(login_url='login')
def home2(request):
    if not request.user.is_authenticated:
        return redirect('login')  

    # Define the stock symbols you're interested in
    stock_symbols = ['SHILPAMED.BO', 'LAURUSLABS.NS', 'ITC.BO', 'MARUTI.BO', 'LT.BO']

    # Fetch the latest date for each stock symbol
    latest_dates = StockData.objects.filter(
        stock_symbol__in=stock_symbols
    ).values('stock_symbol').annotate(latest_date=Max('date'))

    # Prepare a list to hold the latest stock data for each stock symbol
    stock_data = []
    historical_data = {}  # To store historical data for each stock

    # Fetch the latest stock entry for each symbol and historical data
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
                'change': round(change, 2)  # Round the change to 2 decimal places
            })

            # Fetch historical data for the stock (last 30 days)
            historical_data[stock.stock_symbol] = StockData.objects.filter(
                stock_symbol=stock.stock_symbol
            ).order_by('-date')[:30].values('date', 'close')

    # Fetch stock market news from Google News RSS Feed
    query = "Indian stock market"
    encoded_query = quote(query)  # Encode the query parameter
    url = f"https://news.google.com/rss/search?q={encoded_query}"
    feed = feedparser.parse(url)

    # Prepare news data
    news_data = []
    for entry in feed.entries[:10]:  # Limit to 5 news items
        news_data.append({
            'title': entry.title,
            'link': entry.link,
            'published': entry.published
        })

    return render(request, 'pages/home2.html', {
        'stock_data': stock_data,
        'historical_data': historical_data,
        'news_data': news_data  # Pass news data to the template
    })

def home1(request):
    # Fetch the latest 20 unique stocks by date

    if request.user.is_authenticated:
        return redirect('home2/')
    
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

@login_required(login_url='login')
def calculators(request):
    if not request.user.is_authenticated:
        return redirect('login')  
    
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
    if not request.user.is_authenticated:
        return redirect('login/')  # Replace 'login' with your login page URL

    try:
        # Fetch the latest entry for each stock in the user's watchlist
        watchlist = (
            Watchlist.objects.filter(user=request.user)
            .select_related('stock_data')
            .values('stock_data__stock_symbol')
            .annotate(
                latest_date=Max('stock_data__date')
            )
            .order_by('stock_data__stock_symbol')
        )

        # Fetch the latest entry for all available stocks
        available_stocks = (
            StockData.objects.values('stock_symbol')
            .annotate(latest_date=Max('date'))
            .order_by('stock_symbol')
        )
    except Exception as e:
        print(f"Error: {e}")
        return render(request, 'error.html')  # Custom error page to handle the error gracefully

    return render(request, 'pages/dashboard.html', {
        'watchlist': watchlist,
        'available_stocks': available_stocks,
    })

def add_to_watchlist(request):
    if request.method == 'POST':
        stock_symbol = request.POST.get('stock_symbol')
        stock_data = StockData.objects.filter(stock_symbol=stock_symbol).first()
        
        if stock_data:
            Watchlist.objects.get_or_create(user=request.user, stock_data=stock_data)
            messages.success(request, f"{stock_symbol} added to your watchlist.")
        else:
            messages.error(request, "Invalid stock symbol.")
        
        return redirect('dashboard')
    return redirect('dashboard')

def stock_detail(request, stock_symbol):
    # Fetch stock data
    stock_data = StockData.objects.filter(stock_symbol=stock_symbol).order_by('-date')
    if not stock_data.exists():
        return render(request, 'error.html', {'message': f"No data found for stock symbol: {stock_symbol}"})

    # Compute 52-week high/low
    high_52week = stock_data.aggregate(Max('high'))['high__max']
    low_52week = stock_data.aggregate(Min('low'))['low__min']
    latest_data = stock_data.first()

    # Paginate the historical data
    paginator = Paginator(stock_data, 10)  # Show 10 records per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Fetch news related to the stock symbol
    query = f"{stock_symbol} stock"  # Example: "RELIANCE stock"
    encoded_query = quote(query)  # Encode the query parameter
    url = f"https://news.google.com/rss/search?q={encoded_query}"
    feed = feedparser.parse(url)

    # Prepare news data
    news_data = []
    for entry in feed.entries[:8]:  # Limit to 5 news items
        news_data.append({
            'title': entry.title,
            'link': entry.link,
            'published': entry.published
        })

    context = {
        'stock_symbol': stock_symbol,
        'latest_data': latest_data,
        'high_52week': high_52week,
        'low_52week': low_52week,
        'page_obj': page_obj,
        'news_data': news_data,  # Pass news data to the template
    }

    return render(request, 'pages/stock_detail.html', context)

def remove_from_watchlist(request):
    if request.method == 'POST':
        stock_symbol = request.POST.get('stock_symbol')
        try:
            # Find the stock in the user's watchlist and delete it
            watchlist_item = Watchlist.objects.filter(
                user=request.user,
                stock_data__stock_symbol=stock_symbol
            ).first()

            if watchlist_item:
                watchlist_item.delete()
                messages.success(request, f"{stock_symbol} removed from your watchlist.")
            else:
                messages.error(request, "Stock not found in your watchlist.")
        except Exception as e:
            print(f"Error: {e}")
            messages.error(request, "An error occurred while removing the stock.")

        return redirect('dashboard')
    return redirect('dashboard')