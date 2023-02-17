from django.shortcuts import render, redirect, get_object_or_404
from .models import Genre, Book, User
from .forms import BlankForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.


def home(request):
    return render(request, 'synopsis/home.html', {})


def dashboard(request):
    genre_list = Genre.objects.all().order_by('genre')
    form = BlankForm
    if request.method == 'POST':
        # obtain the vlaue of the button pressed, this value is taken from
        # the queary dictionary which has the CSRF token and the name
        # of the button pressed on the dashobard.html
        genre_id = list(request.POST)[1]
        return synopsis(request, genre_id)
    else:
        return render(request, 'synopsis/dashboard.html',
                      {'form': form, 'genre_list': genre_list})


def synopsis(request, genre_id):
    display_books = Book.objects.all().filter(genre=genre_id).order_by()
    genre_name = Genre.objects.get(id=genre_id).genre
    if display_books.exists():
        return render(request, 'synopsis/synopsis.html',
                      {'display_books': display_books})
    else:
        messages.success(request, (
            "Unfortunatly there wheren't any new realeases for " + str(genre_name) + " in this month..."))
        return redirect('dashboard')


def book_info(request, book_id):
    book = Book.objects.get(pk=book_id)
    liked = False
    if book.liked_by.filter(id=request.user.id).exists():
        liked = True
    # show the books infor using the primary key from the genres page.
    return render(request, 'synopsis/book_info.html', {'book': book, 'liked': liked})


'''
def synopsis_redirect(request, book):
    genre = book.genre.id
    print(genre)
    return synopsis(request, genre)
'''


def like_view(request, id):
    book = get_object_or_404(Book, id=request.POST.get('book.id'))
    member = request.user.member
    liked = False
    if book.liked_by.filter(id=request.user.id).exists():
        member.liked_books.remove(book.id)
        book.liked_by.remove(request.user.id)
        liked = False
    else:
        member.liked_books.add(book.id)
        book.liked_by.add(request.user.id)
        liked = True
    return HttpResponseRedirect(reverse('book_info', args=str(id)))


def my_books(request):
    if request.user.is_authenticated:
        my_books = Book.objects.filter(liked_by=request.user.id)
        return render(request, 'synopsis/my_books.html', {'my_books': my_books})
    else:
        messages.success(request, (
            "You must be logged in to view this page"))
        return redirect('home')
