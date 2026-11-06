from django.contrib import admin
from .models import Court, Tariff, ClubInfo


class TariffInline(admin.TabularInline):
    model = Tariff
    extra = 1


@admin.register(Court)
class CourtAdmin(admin.ModelAdmin):
    list_display = ['name', 'court_type', 'is_active']
    inlines = [TariffInline]


@admin.register(ClubInfo)
class ClubInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'opening_time', 'closing_time']

    def has_add_permission(self, request):
        return not ClubInfo.objects.exists()  # singleton, enforced in the admin UI too
