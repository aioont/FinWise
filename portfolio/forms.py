# forms.py
from django import forms
from .models import Investment

class InvestmentForm(forms.ModelForm):
    class Meta:
        model = Investment
        fields = ['name', 'symbol', 'quantity', 'purchase_price']

