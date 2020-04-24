from .models import Activation
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegisterationForm, AccountUpdateForm
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
import datetime
from django.utils.crypto import get_random_string
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user

# Create your views here.


@login_required(login_url='login')
def home_page(request):
    return render(request, 'home.html')


@unauthenticated_user
def register_page(request):
    if request.method == 'POST':
        form = UserRegisterationForm(request.POST, request.FILES)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.is_active = False
            new_user.save()
            token = get_random_string(length=32)
            Activation.objects.create(token=token, user=new_user)
            # Send Confirmation Email
            subject = "please, Confirm Your Email to be able to login"
            message = f'''
                Thank you for your registration,
                please click this link below to confirm your email.
                http://127.0.0.1:8000/{token}
            '''
            from_email = settings.EMAIL_HOST_USER
            to_list = [request.POST['email'], from_email]
            send_mail(subject, message, from_email, to_list, fail_silently=False)

            username = form.cleaned_data.get('username')
            messages.success(request,
                             f'Wonderful {username}, account has been created!, kindly check your email address to activate your account')
            return redirect('home')
    else:
        form = UserRegisterationForm()
    return render(request, 'register.html', {'form': form})


@unauthenticated_user
def login_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'email OR password is incorrect')
    context = {}
    return render(request, 'login.html', context)


def logout_page(request):
    logout(request)
    return redirect('login')


def activate(req, token):
    activation = get_object_or_404(Activation, token=token)
    is_valid = (timezone.now() - activation.created_at) < datetime.timedelta(hours=24)
    if is_valid and not activation.is_used:
        activation.is_used = True
        activation.save()
        activation.user.is_active = True
        activation.user.save()
        messages.success(req, "Great, your account has been activated ")
    else:
        messages.error(req, "Sorry, your activation is not valid OR may be used before,Please try again later")
    return redirect("login")


@login_required(login_url='login')
def account_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    context = {}
    if request.POST:
        form = AccountUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Account has been updated successfully")
    else:
        form = AccountUpdateForm(
            initial={
                'email': request.user.email,
                'username': request.user.username,
                'profile_picture': request.user.profile_picture
            }
        )
    context['account_form'] = form
    return render(request, 'profile.html', context)
