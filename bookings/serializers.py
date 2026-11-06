from rest_framework import serializers
from .models import Booking, NotificationSubscription
from courts.models import Court


class BookingSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Booking
        fields = ['id', 'user', 'court', 'date', 'start_time', 'end_time', 'status', 'created_at']
        read_only_fields = ['status', 'created_at']

    def validate(self, data):
        court = data['court']
        if court.court_type == Court.CourtType.VIP:
            raise serializers.ValidationError('Court 1 is VIP, bookings go through the operations manager.')
        if data['start_time'] >= data['end_time']:
            raise serializers.ValidationError('start_time must be before end_time.')

        overlapping = Booking.objects.filter(
            court=court, date=data['date'],
            status__in=[Booking.Status.PENDING, Booking.Status.CONFIRMED],
            start_time__lt=data['end_time'], end_time__gt=data['start_time'],
        )
        if overlapping.exists():
            raise serializers.ValidationError('This slot overlaps with an existing booking.')
        return data


class NotificationSubscriptionSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = NotificationSubscription
        fields = ['id', 'user', 'court', 'date', 'start_time', 'end_time', 'is_notified', 'created_at']
        read_only_fields = ['is_notified', 'created_at']