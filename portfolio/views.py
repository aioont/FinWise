import random

from .models import Portfolio, Investment

from income.models import Income
from expenses.models import Expense
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect,  get_object_or_404
from django.views import View
from django.contrib import messages
from .forms import InvestmentForm  # You need to create a form for adding investments
import requests
from bs4 import BeautifulSoup
import random
import logging
from decimal import Decimal



class PortfolioView(View):
    def update_investment_data(self, investment):
        try:
            current_price = random.uniform(1, 100)
            investment.current_price = current_price
            investment.total_price = current_price * investment.quantity
            investment.save()
        except Exception as e:
            logging.error(f"Error updating data for {investment.symbol}: {e}")

    def get_nifty_data(self):
        url = "https://www.nseindia.com/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find the tab for "NIFTY BANK" and extract the relevant data
            nifty_bank_tab = soup.find('a', {'id': 'tabList_NIFTYBANK'})
            nifty_bank_value = nifty_bank_tab.find('p', class_='tb_val').text.strip()
            nifty_bank_change = nifty_bank_tab.find('p', class_='tb_per').text.strip()

            # Find the tab for "NIFTY NEXT 50" and extract the relevant data
            nifty_next50_tab = soup.find('a', {'id': 'tabList_NIFTYNEXT50'})
            nifty_next50_value = nifty_next50_tab.find('p', class_='tb_val').text.strip()
            nifty_next50_change = nifty_next50_tab.find('p', class_='tb_per').text.strip()

            # Find the tab for "NIFTY MIDCAP SELECT" and extract the relevant data
            nifty_midcap_tab = soup.find('a', {'id': 'tabList_NIFTYMIDCAPSELECT'})
            nifty_midcap_value = nifty_midcap_tab.find('p', class_='tb_val').text.strip()
            nifty_midcap_change = nifty_midcap_tab.find('p', class_='tb_per').text.strip()

            # Find the tab for "NIFTY FINANCIAL SERVICES" and extract the relevant data
            nifty_financial_tab = soup.find('a', {'id': 'tabList_NIFTYFINANCIALSERVICES'})
            nifty_financial_value = nifty_financial_tab.find('p', class_='tb_val').text.strip()
            nifty_financial_change = nifty_financial_tab.find('p', class_='tb_per').text.strip()


            return {
                'nifty_bank_value': nifty_bank_value,
                'nifty_bank_change': nifty_bank_change,
                'nifty_next50_value': nifty_next50_value,
                'nifty_next50_change': nifty_next50_change,
                'nifty_midcap_value': nifty_midcap_value,
                'nifty_midcap_change': nifty_midcap_change,
                'nifty_financial_value': nifty_financial_value,
                'nifty_financial_change': nifty_financial_change,
            }
        else:
            print("Failed to retrieve Nifty data. Status code:", response.status_code)
            return {}

    def update_investments_data(self, investments):
        for investment in investments:
            self.update_investment_data(investment)

    def get(self, request):
        user_portfolio, created = Portfolio.objects.get_or_create(user=request.user)
        investments = Investment.objects.filter(user=request.user)

        incomes=Income.objects.filter(owner=request.user)
        expenses= Expense.objects.filter(owner=request.user)

        self.update_investments_data(investments)

        total_portfolio_value = sum(investment.total_price for investment in investments if investment.total_price is not None)
        total_invested = sum(investment.invested for investment in investments if investment.invested is not None)
        total_current_investment = sum(investment.current_investment for investment in investments if investment.current_investment is not None)
        total_profit_loss = sum(investment.profit_loss for investment in investments if investment.profit_loss is not None)
        total_balance = sum(Decimal(income.amount) for income in incomes) - sum(Decimal(expensesi.amount) for expensesi in expenses)


        context = {
            'investments': investments,
            'portfolio_value': total_portfolio_value,
            'total_invested': total_invested,
            'total_current_investment': total_current_investment,
            'total_profit_loss': total_profit_loss,
            'total_balance': total_balance,
            'nifty_data': self.get_nifty_data(),
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