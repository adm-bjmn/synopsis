from django.shortcuts import render
from .models import Genre, Book

# Create your views here.


def home(request):
    return render(request, 'synopsis/home.html', {})


def dashboard(request):
    genre_list = Genre.objects.all()
    return render(request, 'synopsis/dashboard.html', {'genre_list': genre_list})


def book_info(request):
    return render(request, 'book_info.html', {})


# set up each of the genre views ready to start putputting the books on ith separate queray sets.
