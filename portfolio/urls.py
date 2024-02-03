# yourapp/urls.py
from django.urls import path
from .views import PortfolioView, AddInvestmentView,UpdateInvestmentView, RemoveInvestmentView
urlpatterns = [
    path('portfolio/', PortfolioView.as_view(), name='portfolio_home'),
    path('add_investment/', AddInvestmentView.as_view(), name='add_investment'),
    path('update_investment/<int:investment_id>/', UpdateInvestmentView.as_view(), name='update_investment'),
    path('remove_investment/<int:investment_id>/', RemoveInvestmentView.as_view(), name='remove_investment'),
]
