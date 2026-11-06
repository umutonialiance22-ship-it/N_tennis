from django.db import models

# Create your models here.
class Court(models.Model):
    class CourtType(models.TextChoices):
        VIP = 'VIP', 'VIP'
        PUBLIC = 'PUBLIC', 'PUBLIC'

    name = models.CharField(max_length=50)
    court_type = models.CharField(max_length=10, choices=CourtType.choices)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Tariff(models.Model):
    court = models.ForeignKey(Court, on_delete=models.CASCADE, related_name='tariffs')
    label = models.CharField(max_length=50)
    price_per_hour = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f'{self.court.name} - {self.label}: {self.price_per_hour}'
    
class ClubInfo(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    address = models.CharField(max_length=255, blank=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    
    def save(self, *args, **kwargs):
        self.pk = 1  
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
