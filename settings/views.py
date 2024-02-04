from django.shortcuts import render, redirect
import json
import os
from .models import Setting
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required

# Create your views here.


def index(request):
    data = []
    file = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(settings.BASE_DIR, 'currencies.json')
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        arr = []
        for key, value in data.items():
            arr.append({'name': key, 'value': value})

    user_obj, created = Setting.objects.get_or_create(user=request.user)

    if request.method == "POST":
        currency = request.POST['currency']
        if not request.POST['currency']:
            messages.error(request, 'ERROR')
            return render(request, 'settings/index.html', context={'currencies': arr, 'settings': user_obj})

        Setting.objects.filter(user=request.user).update(currency=currency)

    messages.success(request, 'Changes saved successfully')

    return render(request, 'settings/index.html', context={'currencies': arr, 'settings': user_obj})


def account(request):
    return render(request, 'settings/account.html')

@login_required
def update_account(request):
    if request.method == 'POST':
        # Get the form data
        full_name = request.POST['full_name']
        last_name = request.POST['last_name']

        # Update the user's additional information
        request.user.first_name = full_name
        request.user.last_name = last_name
        request.user.save()

        messages.success(request, 'Account information updated successfully!')
        return redirect('account-settings')

    return render(request, 'settings/update_account.html')

