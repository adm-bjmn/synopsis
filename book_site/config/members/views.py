from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from .forms import RegisterUserForm, EditProfileForm, ChangeUserPassword
from .models import User
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
        return render(request, 'members/login.html', {})


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
    return render(request, 'members/register.html', {'form': form, })


def user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'members/profile.html', {'user': user, })


def update_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    form = EditProfileForm(request.POST or None, instance=user)
    if form.is_valid():
        form.save()
        return redirect('profile', user_id)
    else:
        return render(request, 'members/update_profile.html', {'user': user, 'form': form})


def change_password(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = ChangeUserPassword(data=request.POST, user=user)
        if form.is_valid():
            form.save()
            messages.success(
                request, (f'Welcome {user}! \n Lets find you something to read...'))
            return redirect('profile', user_id)
    else:
        form = ChangeUserPassword(user=user)
    return render(request, 'members/change_password.html', {'form': form, })
