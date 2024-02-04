from .views import index, account, update_account
from django.urls import path

urlpatterns = [
    path('general', index, name="general-settings"),
    path('account', account, name="account-settings"),
    path('update_account/', update_account, name='update_account'),
]