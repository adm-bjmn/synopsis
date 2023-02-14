from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm

# Create your views here.


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(
                request, (f'Logged in as {user}'))
            return redirect('dashboard')  # redirect to genres
        else:
            messages.success(request, ('No soz...'))
            return redirect('login_user')
    else:
        return render(request, 'registration/login.html', {})


def logout_user(request):
    logout(request)
    # messages.success(request, ('great cheers...'))
    return redirect('home')


def register_user(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(
                request, (f'Welcome {user}! \n Lets find you something to read...'))
            return redirect('dashboard')
    else:
        form = RegisterUserForm()
    return render(request, 'registration/register.html', {'form': form, })
