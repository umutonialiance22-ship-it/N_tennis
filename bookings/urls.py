from rest_framework.routers import DefaultRouter
from .views import BookingViewSet, NotificationSubscriptionViewSet

router = DefaultRouter()
router.register('bookings', BookingViewSet, basename='booking')
router.register('notifications/subscribe', NotificationSubscriptionViewSet, basename='notification-subscription')

urlpatterns = router.urls