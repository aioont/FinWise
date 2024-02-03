from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import Expense, Category
from settings.models import Setting


@login_required(login_url='/authentication/login')
def expenses(request):

    if not Setting.objects.filter(user=request.user).exists():
        messages.info(request, 'Please choose your preferred currency')
        return redirect('general-settings')
    categories = Category.objects.all()
    expenses = Expense.objects.filter(owner=request.user)
    paginator = Paginator(expenses, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    currency = Setting.objects.get(user=request.user).currency
    context = {
        'currency': currency.split('-')[0],
        'categories': categories,
        'expenses': expenses,
        'page_obj': page_obj,
    }
    return render(request=request, template_name='expenses/index.html', context=context)
