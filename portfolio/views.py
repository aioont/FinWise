import random

from .models import Portfolio, Investment
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect,  get_object_or_404
from django.views import View
from django.contrib import messages
from .forms import InvestmentForm  # You need to create a form for adding investments

class PortfolioView(View):
    def get(self, request):
        user_portfolio, created = Portfolio.objects.get_or_create(user=request.user)
        investments = Investment.objects.filter(user=request.user)

        total_portfolio_value = 0

        for investment in investments:
            try:
                # Replace real-time data with random values
                current_price = random.uniform(1, 100)  # Generate a random value between 1 and 100
                investment.current_price = current_price
                investment.total_price = current_price * investment.quantity  # Corrected calculation
                investment.save()
                total_portfolio_value += investment.total_price  # Use total_price in the calculation
            except Exception as e:
                print(f"Error fetching real-time data for {investment.symbol}: {e}")

        context = {
            'investments': investments,
            'portfolio_value': total_portfolio_value,
        }
        return render(request, 'portfolio/portfolio.html', context)

class AddInvestmentView(View):
    template_name = 'portfolio/add_investment.html'

    def get(self, request):
        form = InvestmentForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = InvestmentForm(request.POST)

        if form.is_valid():
            investment = form.save(commit=False)
            investment.user = request.user
            investment.save()

            messages.success(request, 'Investment added successfully.')
            return redirect('portfolio_home')  # Change 'portfolio' to your portfolio URL name

        return render(request, self.template_name, {'form': form})
    

class UpdateInvestmentView(View):
    template_name = 'portfolio/update_investment.html'

    def get(self, request, investment_id):
        investment = get_object_or_404(Investment, id=investment_id, user=request.user)
        form = InvestmentForm(instance=investment)
        return render(request, self.template_name, {'form': form, 'investment': investment})

    def post(self, request, investment_id):
        investment = get_object_or_404(Investment, id=investment_id, user=request.user)
        form = InvestmentForm(request.POST, instance=investment)

        if form.is_valid():
            form.save()
            messages.success(request, 'Investment updated successfully.')
            return redirect('portfolio_home')  # Change 'portfolio' to your portfolio URL name

        return render(request, self.template_name, {'form': form, 'investment': investment})
    
class RemoveInvestmentView(View):
    template_name = 'portfolio/remove_investment.html'

    def get(self, request, investment_id):
        investment = get_object_or_404(Investment, id=investment_id, user=request.user)
        return render(request, self.template_name, {'investment': investment})

    def post(self, request, investment_id):
        investment = get_object_or_404(Investment, id=investment_id, user=request.user)
        investment.delete()
        messages.success(request, 'Investment removed successfully.')
        return redirect('portfolio_home')