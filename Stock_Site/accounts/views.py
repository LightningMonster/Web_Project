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
import yfinance as yf

# Function to fetch live stock price
def fetch_live_stock_price(ticker):
    try:
        # Fetch the stock data using yfinance
        stock = yf.Ticker(ticker)

        # Get the live price (current price)
        live_price = stock.history(period="1d", interval="1m")["Close"][-1]  # Get the latest closing price for the 1-minute interval

        # Return the live price
        return live_price

    except Exception as e:
        # Handle errors (e.g., ticker not found)
        print(f"Error fetching live price for {ticker}: {e}")
        return None

def login_user(request):
    if request.method == 'POST':
        if 'register' in request.POST:  # Registration Form Submission
            username = request.POST.get('username')
            email = request.POST.get('email')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            if password != confirm_password:
                messages.error(request, 'Passwords do not match')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email is already registered')
            elif User.objects.filter(username=username).exists():
                messages.error(request, 'Username is already taken')
            else:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    password=password
                )
                user.save()
                messages.success(request, 'Registration successful. Please log in.')
                return redirect('home1')  # Redirect to login page after registration

        else:  # Login Form Submission
            email = request.POST.get('email')
            password = request.POST.get('password')

            try:
                user = User.objects.get(email=email)
                user = authenticate(request, username=user.username, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Login successful')
                    return redirect('home2')
                else:
                    messages.error(request, 'Invalid email or password')
            except User.DoesNotExist:
                messages.error(request, 'Invalid email or password')

    return render(request, 'accounts/login.html')  # Single template for both

def logout_user(request):
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('/')

@login_required(login_url='login')
def home2(request):
    if not request.user.is_authenticated:
        return redirect('login')
        return redirect('login')

    # Fetch all distinct stock symbols from the database
    all_stock_symbols = StockData.objects.values_list('stock_symbol', flat=True).distinct()

    stock_data = []  # Trending stocks (Top 5 by volume)
    gainers_losers_data = []  # Stores all stocks for gainers/losers sorting
    historical_data = {}
    
    # Get the latest entry for each stock symbol (sorted by volume)
    latest_entries = StockData.objects.filter(
        stock_symbol__in=all_stock_symbols
    ).order_by('-date', '-volume')[:5]  # Top 5 stocks by volume

    for stock in all_stock_symbols:
        # Fetch last two entries for the stock symbol
        last_two_entries = StockData.objects.filter(
            stock_symbol=stock
        ).order_by('-date')[:2]

        if len(last_two_entries) == 2:
            previous_close = last_two_entries[1].close
            current_close = last_two_entries[0].close
            change = ((current_close - previous_close) / previous_close) * 100 if previous_close else 0

            # Store all stocks for gainers/losers selection
            gainers_losers_data.append({
                'symbol': last_two_entries[0].stock_symbol,
                'change': round(change, 2)  # Calculating change here
            })

            # Fetch historical data (last 30 days)
            historical_data[last_two_entries[0].stock_symbol] = StockData.objects.filter(
                stock_symbol=last_two_entries[0].stock_symbol
            ).order_by('-date')[:30].values('date', 'close')

    # Select **Top 5 Stocks by Volume** for Trending Section
    for stock in latest_entries:
        last_two_entries = StockData.objects.filter(
            stock_symbol=stock.stock_symbol
        ).order_by('-date')[:2]
        
        if len(last_two_entries) == 2:
            previous_close = last_two_entries[1].close
            current_close = last_two_entries[0].close
            change = ((current_close - previous_close) / previous_close) * 100 if previous_close else 0

            # Fetch live price for the stock
            live_price = fetch_live_stock_price(stock.stock_symbol)

            # Add live price to the stock data
            stock_data.append({
                'symbol': stock.stock_symbol,
                'last_price': current_close,
                'change': round(change, 2),  # Calculating change here
                'volume': stock.volume,
                'live_price': live_price if live_price else current_close  # Fallback to last_close if live price is unavailable
            })

    # Sort all stocks for gainers/losers selection
    sorted_gainers = sorted(gainers_losers_data, key=lambda x: x['change'], reverse=True)[:5]
    sorted_losers = sorted(gainers_losers_data, key=lambda x: x['change'])[:5]

    # Fetch live prices for gainers and losers
    for stock in sorted_gainers:
        live_price = fetch_live_stock_price(stock['symbol'])
        stock['live_price'] = live_price if live_price else None

    for stock in sorted_losers:
        live_price = fetch_live_stock_price(stock['symbol'])
        stock['live_price'] = live_price if live_price else None

    # Fetch stock market news from Google News RSS Feed
    query = "Indian stock market"
    encoded_query = quote(query)
    encoded_query = quote(query)
    url = f"https://news.google.com/rss/search?q={encoded_query}"
    feed = feedparser.parse(url)

    # Prepare news data
    news_data = []  # Limit to 10 news items
    for entry in feed.entries[:10]:  # Limit to 10 news items
        news_data.append({
            'title': entry.title,
            'link': entry.link,
            'published': entry.published
        })

    return render(request, 'pages/home2.html', {
        'all_stocks': all_stock_symbols,  # Pass all stock symbols
        'stock_data': stock_data,  # Top 5 stocks by volume
        'historical_data': historical_data,
        'news_data': news_data,
        'top_gainers': sorted_gainers,  # Top 5 gainers with live price
        'top_losers': sorted_losers  # Top 5 losers with live price
    })



def home1(request):
    # Redirect authenticated users to 'home2/'
    if request.user.is_authenticated:
        return redirect('home2/')

    # Fetch the latest 8 unique stocks ending with '.NS' by date
    stocks = (
        StockData.objects.filter(stock_symbol__endswith='.BO')
        .order_by('stock_symbol', '-date')
        .distinct('stock_symbol')[:8]
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

    # Fetch additional company details (assuming they are stored in the latest_data object)
    company_name = latest_data.company_name
    ceo = latest_data.ceo
    headquarters = latest_data.headquarters
    industry = latest_data.industry
    sector = latest_data.sector
    website = latest_data.website
    dividend_yield = latest_data.dividend_yield
    eps = latest_data.eps
    market_cap = latest_data.market_cap
    pe_ratio = latest_data.pe_ratio

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
    for entry in feed.entries[:8]:  # Limit to 8 news items
        news_data.append({
            'title': entry.title,
            'link': entry.link,
            'published': entry.published
        })

    # Prepare context with all fields
    context = {
        'stock_symbol': stock_symbol,
        'latest_data': latest_data,
        'high_52week': high_52week,
        'low_52week': low_52week,
        'page_obj': page_obj,
        'news_data': news_data,
        'company_name': company_name,
        'ceo': ceo,
        'headquarters': headquarters,
        'industry': industry,
        'sector': sector,
        'website': website,
        'dividend_yield': dividend_yield,
        'eps': eps,
        'fifty_two_week_high': high_52week,  # Same as high_52week
        'fifty_two_week_low': low_52week,    # Same as low_52week
        'market_cap': market_cap,
        'pe_ratio': pe_ratio,
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

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    return render(request, 'pages/profile.html')

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def search_stocks(request):
    query = request.GET.get("q", "").strip()
    if not query:
        return JsonResponse({"stocks": []})

    results = StockData.objects.filter(company_name__icontains=query).values("company_name", "stock_symbol")[:1]  # Limit results

    return JsonResponse({"stocks": list(results)})

def admin(request):
    return render(request, 'accounts/admin.html')
