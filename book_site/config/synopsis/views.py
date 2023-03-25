from django.shortcuts import render, redirect, get_object_or_404
from .models import Genre, Book, User
from .forms import UpdateBookForm, BlankForm, GenreForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q

from django.core.paginator import Paginator
# Create your views here.


def home(request):
    return render(request, 'synopsis/home.html', {})


def dashboard(request):
    genre_list = Genre.objects.all().order_by('genre')
    if request.method == 'POST':
        form = GenreForm(request.POST)
        if form.is_valid():
            selected_genres = form.cleaned_data.get('selected_genres')
            print(f'form_selected: {type(selected_genres)}')
            selected_genres = '-'.join(selected_genres)

        return redirect(synopsis, selected_genres)
        # return redirect('dashboard')
    else:
        form = GenreForm()
        return render(request, 'synopsis/dashboard.html',
                      {'form': form, 'genre_list': genre_list})


def synopsis(request, selected_genres):
    selected_genres = selected_genres.split('-')
    print(f'selected genres: {selected_genres}')
    print(f'selected type: {type(selected_genres)}')
    display_books = (Book.objects.all().filter(
        genre__in=selected_genres)).exclude(
            liked_by=request.user.id).order_by('?').distinct()
    print(f'DISPLAY BOOKS: {display_books}')
    print(len(display_books))
    # display books = display_books.remove if seen_by == user.id
    selected_genres = '-'.join(selected_genres)
    request.session['selected_genres'] = selected_genres
    if display_books.exists():
        p_n = Paginator(display_books, 1)
        page = request.GET.get('page')
        pages = p_n.get_page(page)
        return render(request, 'synopsis/synopsis.html',
                      {'pages': pages, 'selected_genres': selected_genres})
    else:
        messages.success(request, (
            "You've seen all there is to see for " + str(genre_name) + " this month, check back soon for more new realeases."))
        return redirect('dashboard')


def book_info(request, book_id):
    selected_genres = request.session.get('selected_genres')
    book = Book.objects.get(pk=book_id)
    liked = False
    if book.liked_by.filter(id=request.user.id).exists():
        liked = True
    # get book genres and output them to the contexts dictionary.
    # try to figure out how to get a back button.
    # show the books infor using the primary key from the genres page.
    return render(request, 'synopsis/book_info.html', {'book': book, 'liked': liked, 'selected_genres': selected_genres})


def like_view(request, id):
    book_id = str(id)
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
    return HttpResponseRedirect(reverse('book_info', kwargs={'book_id': book_id}))


def my_books(request):
    if request.user.is_authenticated:
        my_books = Book.objects.filter(
            liked_by=request.user.id)
        return render(request, 'synopsis/my_books.html', {'my_books': my_books})
    else:
        messages.success(request, (
            "You must be logged in to view this page"))
        return redirect('home')


def search_book(request):
    if request.method == "POST":
        criteria = request.POST['criteria']
        book_to_update = Book.objects.filter(
            Q(id__contains=criteria) |
            Q(title__contains=criteria) |
            Q(author__contains=criteria)
        ).first()
        return render(request, 'synopsis/search_book.html', {'criteria': criteria, 'book_to_update': book_to_update, })
    else:
        return render(request, 'synopsis/search_book.html', {})


def update_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    form = UpdateBookForm(request.POST or None, instance=book)
    if form.is_valid():
        form.save()
        messages.success(
            request, (f'{book.title} has been updated.'))
        return redirect('search_book')
    else:
        return render(request, 'synopsis/update_book.html', {'book': book, 'form': form})
    return render(request, 'synopsis/update_book.html', {'book': book, })


def delete_book(request, book_id):
    book_to_delete = get_object_or_404(Book, id=book_id)
    delete_title = book_to_delete.title
    book_to_delete.delete()
    messages.success(
        request, (f'{delete_title} has been deleted.'))
    return redirect('search_book')


# remove like if the user clicks the button remove the like from the book object and reload the page.
def remove_book(request, book_id):
    book = get_object_or_404(Book, id=request.POST.get('book.id'))
    book.liked_by.remove(request.user.id)
    return redirect('my_books')
