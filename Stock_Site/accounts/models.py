from django.db import models
from django.contrib.auth.models import User

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

    class Meta:
        unique_together = ('stock_symbol', 'date')  # Ensures that a stock symbol and date combination is unique

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock_data = models.ForeignKey(StockData, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'stock_data')