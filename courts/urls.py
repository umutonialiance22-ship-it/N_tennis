from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CourtViewSet, ClubInfoView

router = DefaultRouter()
router.register('', CourtViewSet, basename='court')

urlpatterns = [
    path('club-info/', ClubInfoView.as_view(), name='club-info'),
] + router.urls