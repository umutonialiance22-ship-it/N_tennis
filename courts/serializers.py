from rest_framework import serializers
from .models import Court, Tariff, ClubInfo


class TariffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tariff
        fields = ['id', 'label', 'price_per_hour']


class CourtSerializer(serializers.ModelSerializer):
    tariffs = TariffSerializer(many=True, read_only=True)

    class Meta:
        model = Court
        fields = ['id', 'name', 'court_type', 'description', 'is_active', 'tariffs']


class ClubInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClubInfo
        fields = ['name', 'description', 'address', 'contact_email', 'contact_phone', 'opening_time', 'closing_time']