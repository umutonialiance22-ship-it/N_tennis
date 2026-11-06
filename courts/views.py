from datetime import datetime, timedelta
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from .models import Court, ClubInfo
from .serializers import CourtSerializer, ClubInfoSerializer
from bookings.models import Booking


class CourtViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CourtSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = Court.objects.filter(is_active=True)
        if self.request.user.role != self.request.user.Role.ADMIN:
            qs = qs.exclude(court_type=Court.CourtType.VIP)
        return qs

    @action(detail=True, methods=['get'])
    def availability(self, request, pk=None):
        date_str = request.query_params.get('date')
        if not date_str:
            return Response({'detail': 'date query param required, e.g. ?date=2026-06-20'}, status=400)

        court = self.get_object()
        club = ClubInfo.objects.first()
        booked = list(Booking.objects.filter(
            court=court, date=date_str,
            status__in=[Booking.Status.PENDING, Booking.Status.CONFIRMED],
        ).values('start_time', 'end_time'))

        slots, current = [], datetime.combine(datetime.today(), club.opening_time)
        end_of_day = datetime.combine(datetime.today(), club.closing_time)
        while current < end_of_day:
            slot_end = current + timedelta(hours=1)
            is_booked = any(b['start_time'] <= current.time() < b['end_time'] for b in booked)
            slots.append({
                'start_time': current.time().strftime('%H:%M'),
                'end_time': slot_end.time().strftime('%H:%M'),
                'is_available': not is_booked,
            })
            current = slot_end

        return Response({'court': court.name, 'date': date_str, 'slots': slots})


class ClubInfoView(RetrieveAPIView):
    serializer_class = ClubInfoSerializer
    permission_classes = [permissions.AllowAny]

    def get_object(self):
        return ClubInfo.objects.first()
