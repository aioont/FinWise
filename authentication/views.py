from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
import threading
from .utils import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.conf import settings
from django.views.generic import View
from django.http import JsonResponse
from validate_email import validate_email
import json

# Create your views here.
class EmailThread(threading.Thread):
    def __init__(self, subject, html_content, from_email, recipient_list):
        self.subject = subject
        self.recipient_list = recipient_list
        self.html_content = html_content
        self.from_email = from_email
        threading.Thread.__init__(self)

    def run(self):
        send_mail(message=self.html_content, from_email=settings.EMAIL_HOST_USER, subject=self.subject,
                  recipient_list=[self.recipient_list])


class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data.get('username', '')
        if not str(username).isalnum():
            return JsonResponse({'error': 'username can  only contain letters and numbers'})
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'username is taken,please choose a new one'})
        return JsonResponse({'is_available': 'true'})


class CredentialsValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data.get('email', '')
        if not email:
            return JsonResponse({'error': 'Please enter an email'})
        is_valid = validate_email(email)
        if not is_valid:
            return JsonResponse({'error': 'Please enter a valid email'})
        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Email is taken,please choose a new one'})
        return JsonResponse({'valid': True})


class RegistrationView(View):
    def post(self, request):
        # Get form values
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        # Check username
        if User.objects.filter(username=username).exists():
            messages.error(request, 'This username is already taken')
            return redirect('register')
        else:
            if User.objects.filter(email=email).exists():
                messages.error(request, 'This email is being used')
                return redirect('register')
            else:
                user = User.objects.create_user(
                    username=username, password=password, email=email)
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                email_subject = 'Activate Your Account'
                message = render_to_string('authentication/activate_account.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                EmailThread(subject=email_subject, from_email=settings.EMAIL_HOST_USER,
                            html_content=message, recipient_list=user.email).start()
                messages.add_message(request, messages.SUCCESS, 'Account created successfully,please visit your email to '

  'verify your Account')
                return redirect('login')

    def get(self, request):
        return render(request, 'authentication/register.html')


class LoginView(View):
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            if user.is_active == True:
                auth.login(request, user)
                messages.success(request, 'You are now logged in')
                return redirect('expenses')
            else:
                messages.error(request, 'Email is not verified')
                return redirect('login')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')

    def get(self, request):
        return render(request, 'authentication/login.html')

