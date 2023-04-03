from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from .forms import RegisterUserForm, EditProfileForm, ChangeUserPassword
from .models import User, Member
from synopsis.models import Book
from django.urls import reverse
from django.http import HttpResponseRedirect
from synopsis import urls, views

# Create your views here.


def login_user(request):
    ''' Utilising built in django authentication'''
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # redirect to genres
        else:
            messages.success(request, ('Login in Failed.'))
            return redirect('login_user')
    else:
        return render(request, 'members/login.html', {})


def logout_user(request):
    ''' Utilising built in django authentication'''
    logout(request)
    # messages.success(request, ('great cheers...'))
    return redirect('home')


def register_user(request):
    ''' Utilising built in django authentication,
    Register user creates a django built in User object
    as well as an associated members object
    by using the built in django create user function. 
    '''
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegisterUserForm()
    return render(request, 'members/register.html', {'form': form, })


def user_profile(request, user_id):
    member = request.user.member
    ''' Simple view to show a user their profile information in profile.html'''
    user = get_object_or_404(User, id=user_id)
    return render(request, 'members/profile.html', {'user': user, 'member': member})


def update_profile(request, user_id):
    ''' Utilising built in django authentication'''
    user = get_object_or_404(User, id=user_id)
    form = EditProfileForm(request.POST or None, instance=user)
    if form.is_valid():
        form.save()
        return redirect('profile', user_id)
    else:
        return render(request, 'members/update_profile.html', {'user': user, 'form': form})


def change_password(request, user_id):
    ''' Utilising built in django authentication'''
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


def delete_user(request, user_id):
    ''' Utilising built in django authentication'''
    user_to_delete = get_object_or_404(User, id=user_id)
    logout(request)
    user_to_delete.delete()
    messages.success(
        request, (f'Your Profile has been deleted.'))
    return redirect('home')


def reset_synopsis(request, user_id):
    user = get_object_or_404(User, id=user_id)
    seen_books = Book.objects.all().filter(seen_by=user)
    for book in seen_books:
        book.seen_by.remove(user)
    messages.success(
        request, (f'Your books have been reset.'))
    return redirect('home')


def toggle_instructions(request, user_id):
    referer = request.META.get('HTTP_REFERER')
    referer = referer.split('/')
    selected_genres = referer[-1].partition('?')[0]

    user = get_object_or_404(User, id=user_id)
    member = request.user.member
    print(member.seen_instructions)
    if member.seen_instructions == False:
        print('The member is false')
        member.seen_instructions = True
        member.save()
        print(member.seen_instructions)
    else:
        print('theember is true')
        member.seen_instructions = False
        member.save()
        print(member.seen_instructions)
    if referer[-2] == "synopsis":
        print(selected_genres)
        return redirect('synopsis', selected_genres)
    else:
        return HttpResponseRedirect(reverse('profile', kwargs={'user_id': user_id}))
