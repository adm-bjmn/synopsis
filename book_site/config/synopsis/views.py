from django.shortcuts import render, redirect
from .models import Genre, Book
from .forms import BlankForm
from django.contrib import messages

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
        print(f'Genre ID = {genre_id}')
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
    # show the books infor using the primary key from the genres page.
    return render(request, 'synopsis/book_info.html', {'book': book, })


def synopsis_redirect(request, book):
    genre = book.genre.id
    print(genre)
    return synopsis(request, genre)
