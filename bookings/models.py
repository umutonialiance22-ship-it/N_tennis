from django.conf import settings
from django.db import models
from courts.models import Court


# Create your models here.
class Booking(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        CONFIRMED = 'CONFIRMED', 'Confirmed'
        CANCELLED = 'CANCELLED', 'Cancelled'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    court = models.ForeignKey(Court, on_delete=models.CASCADE, related_name='bookings')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date', 'start_time']


class NotificationSubscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notification_subscriptions')
    court = models.ForeignKey(Court, on_delete=models.CASCADE, related_name='notification_subscriptions')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_notified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
