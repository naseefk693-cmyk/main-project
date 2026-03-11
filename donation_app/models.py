from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

class FoodDonation(models.Model):
    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Claimed', 'Claimed'),
        ('Collected', 'Collected'),
    ]

    donor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="donations")
    ngo = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="claims")
    food_type = models.CharField(max_length=100)
    quantity = models.CharField(max_length=50)
    expiry_time = models.DateTimeField()
    image = models.ImageField(upload_to="donations/", blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Available")

    donation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    short_id = models.CharField(max_length=8, editable=False, unique=True, null=True, blank=True)

    claimed_at = models.DateTimeField(null=True, blank=True)
    collected_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.short_id:
            # generate first 8 characters of UUID without dashes
            self.short_id = str(self.donation_id).replace("-", "")[:8]
        super().save(*args, **kwargs)

    def is_expired(self):
        return self.expiry_time <= timezone.now()

    def __str__(self):
        return f"{self.food_type} ({self.short_id})"


class DonationMessage(models.Model):
    donation = models.ForeignKey(FoodDonation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message by {self.sender.username} on {self.donation}"
