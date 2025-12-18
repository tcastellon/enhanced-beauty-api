from django.db import models
from django.contrib.auth.models import User

class Service(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

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
    preferred_needle_type = models.CharField(max_length=20, blank=True, null=True)
    preferred_ink_color = models.CharField(max_length=30, blank=True, null=True)
    preference_note = models.TextField(blank=True, null=True)
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
