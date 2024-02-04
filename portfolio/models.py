from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

class Portfolio(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Investment(models.Model):
    name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=10)
    quantity = models.PositiveIntegerField()
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    current_investment = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    @property
    def invested(self):
        return self.purchase_price * self.quantity
    
    @property
    def profit_loss(self):
        # Convert float to Decimal and then subtract
        return Decimal(str(self.total_price)) - self.invested
    
