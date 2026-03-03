from django.core.management.base import BaseCommand
from django.utils import timezone
from donation_app.models import FoodDonation

class Command(BaseCommand):
    help = 'Automatically marks expired food as Expired'
    
    def handle(self, *args, **kwargs):
        expired_items = FoodDonation.objects.filter(status='Available', expiry_time__lt=timezone.now())
        count = expired_items.count()
        expired_items.update(status='Expired')
        self.stdout.write(f"Updated {count} items to Expired status.")

