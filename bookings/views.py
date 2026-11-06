from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Booking, NotificationSubscription
from .serializers import BookingSerializer, NotificationSubscriptionSerializer


class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post', 'delete']

    def get_queryset(self):
        user = self.request.user
        if user.role == user.Role.ADMIN:
            return Booking.objects.all()
        return Booking.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(status=Booking.Status.CONFIRMED)

    def destroy(self, request, *args, **kwargs):
        booking = self.get_object()
        booking.status = Booking.Status.CANCELLED
        booking.save()
        notify_subscribers(booking)
        return Response(status=status.HTTP_204_NO_CONTENT)


class NotificationSubscriptionViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post', 'delete']

    def get_queryset(self):
        return NotificationSubscription.objects.filter(user=self.request.user)


def notify_subscribers(booking):
    matches = NotificationSubscription.objects.filter(
        court=booking.court, date=booking.date,
        start_time__lt=booking.end_time, end_time__gt=booking.start_time,
        is_notified=False,
    )
    for sub in matches:
        sub.is_notified = True
        sub.save()
        # V1 just flags it. Swap this for an actual send (email or push)
        # once you decide on a delivery channel — that's a V2 polish item.