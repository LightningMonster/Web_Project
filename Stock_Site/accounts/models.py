from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

# Stock Data Model
class StockData(models.Model):
    stock_symbol = models.CharField(max_length=50)
    date = models.DateField()
    open = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    high = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    low = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    close = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    volume = models.DecimalField(max_digits=20, decimal_places=2)
    dividends = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock_splits = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    company_name = models.CharField(max_length=255, null=True, blank=True)
    industry = models.CharField(max_length=255, null=True, blank=True)
    sector = models.CharField(max_length=100, null=True, blank=True)
    ceo = models.CharField(max_length=255, null=True, blank=True)
    headquarters = models.CharField(max_length=255, null=True, blank=True)
    website = models.CharField(max_length=255, null=True, blank=True)
    market_cap = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    pe_ratio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    eps = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    dividend_yield = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    fifty_two_week_high = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    fifty_two_week_low = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        unique_together = ('stock_symbol', 'date')  # Ensures that a stock symbol and date combination is unique

    def __str__(self):
        return f"{self.stock_symbol} - {self.date}"

# Watchlist Model (user's stock favorites)
class Watchlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stock_data = models.ForeignKey(StockData, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'stock_data')

    def __str__(self):
        return f"Watchlist: {self.user.username} - {self.stock_data.stock_symbol}"

# Custom User Model (only one definition)
class CustomUser(AbstractUser):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    phone_number = models.CharField(max_length=15, blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)

    def __str__(self):
        return self.username

class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    rating = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.rating}⭐)"
