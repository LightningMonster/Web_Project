from django.core.management.base import BaseCommand
from accounts.models import StockData, Watchlist

class Command(BaseCommand):
    help = 'Clear all data from StockData and Watchlist'

    def handle(self, *args, **kwargs):
        StockData.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('All data cleared from StockData and Watchlist'))
