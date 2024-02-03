from django.shortcuts import render
import json
import os
from .models import Setting
from django.contrib import messages
from django.conf import settings
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