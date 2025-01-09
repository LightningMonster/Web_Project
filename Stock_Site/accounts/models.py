from django.db import models

class StockData(models.Model):
    stock_symbol = models.CharField(max_length=50)
    date = models.DateField()
    open = models.DecimalField(max_digits=20, decimal_places=2)
    high = models.DecimalField(max_digits=20, decimal_places=2)
    low = models.DecimalField(max_digits=20, decimal_places=2)
    close = models.DecimalField(max_digits=20, decimal_places=2)
    volume = models.DecimalField(max_digits=20, decimal_places=2)
    dividends = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    stock_splits = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.stock_symbol} - {self.date}"

