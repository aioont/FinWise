from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User

class Income(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    currency = models.CharField(max_length=20, default="USD")
    created_at = models.DateTimeField(auto_now=True)
    description = models.TextField(default='_')
    income_date = models.DateField(default=timezone.now)
    source = models.CharField(max_length=100, null=False, blank=False, default="Salary")
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.amount)

    class Meta:
        ordering = ['-created_at']


class Source(models.Model):
    name = models.CharField(max_length=20, default="Salary")

    def __str__(self):
        return self.name
