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
from django.db.models import Q
from projects.models import *
# Create your views here.


@login_required(login_url='login')
def home_page(request):
    # end = Project.objects.filter(end_date=end_date)
    # now = timezone.now()
    # query = end < now
    latest_projects = Project.objects.order_by("-id")[:5]
    # if query:
    heigest_rate_projects = Rate.objects.order_by("-body")[:5]
    category_result = Category.objects.all()
    context = {
        "latest_projects":latest_projects,
        "heighest_rate_projects": heigest_rate_projects,
        "category_result":category_result
    }
    return render(request, 'home.html', context)


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
    
    if request.method == 'POST':
        form = AccountUpdateForm(request.POST,request.FILES, instance=request.user)
        if form.is_valid():
            print(request.FILES)
            form.initial = {
            "first_name": request.POST['first_name'],
            "last_name": request.POST['last_name'],
            "email": request.POST['email'],
            "profile_picture": request.POST['profile_picture'],
            "username": request.POST['username'],
            "mobile": request.POST['mobile'],
            "birthdate": request.POST.get('birthdate'),
            "country": request.POST['country'],
            "facebook_profile": request.POST['facebook_profile'],

            }
            form.save()
            messages.success(request, "Account has been updated successfully")
    else:
        form = AccountUpdateForm(
            initial={
                "email": request.user.email,
                "username": request.user.username,
                "profile_picture": request.user.profile_picture,
                "first_name": request.user.first_name,
                "last_name": request.user.last_name,
                "mobile": request.user.mobile,
                "birthdate": request.user.birthdate,
                "country": request.user.country,
                "facebook_profile": request.user.facebook_profile,
            }
        )
    context['account_form'] = form
    return render(request, 'profile.html', context)

def delete_profile(request):
    if request.method == 'GET':
        request.user.delete()
    return redirect('login')
    
    

def projects_view(request , id):
    projects = Project.objects.filter(category_id = id)
    list_projects = {"projects":projects}
    return render(request,"show_projects.html",list_projects)

def search(request):
    query = request.GET.get('q')
    if query:
        title_results = Project.objects.filter(Q(title__icontains=query))
        tag_results = Tag.objects.filter(Q(name__icontains=query))
        context={
            "title_results":title_results,
            "tag_results":tag_results
        }
    else:
        messages = messages.error(request,'no result found')
        context = {"messages":messages}
    return render(request,'home.html', context)
