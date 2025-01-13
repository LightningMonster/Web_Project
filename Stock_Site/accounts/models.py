from django.db import models

class StockData(models.Model):
    stock_symbol = models.CharField(max_length=20)
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

