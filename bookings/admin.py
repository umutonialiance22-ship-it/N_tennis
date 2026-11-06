from django.contrib import admin
from .models import Booking, NotificationSubscription


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'court', 'date', 'start_time', 'end_time', 'status']
    list_filter = ['status', 'court']


@admin.register(NotificationSubscription)
class NotificationSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'court', 'date', 'start_time', 'end_time', 'is_notified']
    