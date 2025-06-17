from django.db import models

# Create your models here.
from django.contrib.auth import get_user_model

from food.custom_auth.models import BaseModel

User = get_user_model()

class Domain(BaseModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Internship(BaseModel):
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    domain = models.ForeignKey(Domain, on_delete=models.SET_NULL, null=True, related_name="internships")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="assigned_students")
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    is_pay = models.BooleanField(default=False)
    is_complete = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.domain}"
