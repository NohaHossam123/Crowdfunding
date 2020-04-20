from django.shortcuts import render, redirect
from .forms import UserRegisterationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required(login_url='login')
def home_page(request):
    return render(request, 'home.html')


def register_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            form = UserRegisterationForm(request.POST)
            if form.is_valid():
                new_user = form.save(commit=False)
                new_user.is_active = True
                new_user.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Thank you for registering in our website' + user)
                # token = get_random_string(length=32)
                # Activation.objects.create(token=token, user=new_user)
                # Send Confirmation Email
                # subject = "Confirm Your Email"
                # message = f'''
                #     Thank you for registering in our website,
                #     please click link below to confirm your email.
                #     http://localhost:8000/auth/activate/{token}
                # '''

                # from_email = settings.EMAIL_HOST_USER
                # to_list = [request.POST['email'], from_email]
                # send_mail(subject, message, from_email, to_list, fail_silently=True)

                # username = form.cleaned_data.get('username')
                # messages.success(request,
                #                  f'Account created for {username}!,Please check your email to activate your account first')
                return redirect('login')
        else:
            form = UserRegisterationForm()
        return render(request, 'register.html', {'form': form})


def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
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