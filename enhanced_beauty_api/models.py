import random
import string
from django.db import models
from django.contrib.auth.models import User

def _generate_booking_reference():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)
    duration = models.PositiveIntegerField(default=30)

    def __str__(self):
        return self.name

class Availability(models.Model):
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    booked = models.BooleanField(default=False)

    class Meta:
        ordering = ['date', 'start_time']
        verbose_name_plural = "Availabilities"

    def __str__(self):
        return f"{self.date} - {self.start_time}"

class Booking(models.Model):
    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('rescheduled', 'Rescheduled')
    ]

    availability = models.OneToOneField(Availability, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    reference = models.CharField(default=_generate_booking_reference, max_length=8, unique=True)
    status = models.CharField(choices=STATUS_CHOICES, default='confirmed', max_length=11)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.availability.date} - {self.availability.start_time}"

class Client(models.Model):
    created_by_user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    street_address = models.CharField(max_length=100)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=5)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    date_of_birth = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Visit(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    created_by_user = models.ForeignKey(User, on_delete=models.CASCADE)
    note_content = models.TextField(blank=True, null=True)
    visit_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.client.name} - {self.visit_date}"

class VisitService(models.Model):
    visit = models.ForeignKey(Visit, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.visit.client.name} - {self.service.name} - {self.visit.visit_date}"
