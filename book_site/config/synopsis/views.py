from django.shortcuts import render, redirect, get_object_or_404
from .models import Genre, Book, User
from .forms import UpdateBookForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q

from django.core.paginator import Paginator
# Create your views here.


def home(request):
    return render(request, 'synopsis/home.html', {})


'''
# ======== FUNCTION BUILD WITH FORM ======== First Version.
def dashboard(request):
    Displays all genres to the logged in user and request a selection
which will be used as the search criteria for the synopsis function
    genre_list = Genre.objects.all()
    if request.method == 'POST':
        form = GenreForm(request.POST)
        if form.is_valid():
            selected_genres = form.cleaned_data.get('selected_genres')
            print(f'form_selected: {type(selected_genres)}')
            selected_genres = '-'.join(selected_genres)
            return redirect(synopsis, selected_genres)
        else:
            # return the form with error messeages
            form = GenreForm(request.POST)
            return render(request, 'synopsis/dashboard.html',
                          {'form': form, 'genre_list': genre_list})
    else:
        form = GenreForm()
        return render(request, 'synopsis/dashboard.html',
                      {'form': form, 'genre_list': genre_list})
'''


def dashboard(request):
    ''' Displays all genres to the logged in user and request a selection
    which will be used as the search criteria for the synopsis function
    '''
    genre_list = Genre.objects.all()
    if request.method == 'POST':
        if len(request.POST.getlist('selected_items')) > 0:
            selected_genres = request.POST.getlist('selected_items')
            print(f'selected Genres: {selected_genres}')
            selected_genres = '-'.join(selected_genres)

            return redirect(synopsis, selected_genres)
        else:
            error = 'error'
            messages.success(request, (
                "You must choose at least one Genre..."))
            return redirect('dashboard')
    else:
        return render(request, 'synopsis/dashboard.html',
                      {'genre_list': genre_list, })


def synopsis(request, selected_genres):
    '''Uses the reponse to the dashboard form as search criteria to search
    for relevant book objects.
    synopsis then shows the user the synopsis of each book one at a time,
    with options to go to next, add to my books or view more details,
    Once the user has seen a book then the seen_by field is checked to
    ensure the book does not re appear in future searches.
    If a book opject is liked_by the the looged in user it will also be
    excluded rom the search resuts.
    Once the user has seen all books in a search they are shown a message
    acknowledging this and given the option to return to the dashboard.
    '''
    member = request.user.member
    selected_genres = selected_genres.split('-')
    # print(f'selected genres: {selected_genres}')
    # print(f'selected type: {type(selected_genres)}')
    display_books = (Book.objects.all().filter(
        genre__in=selected_genres)).exclude(
            liked_by=request.user.id).exclude(
                seen_by=request.user.id)
    # .order_by('?').distinct()
    # display books = display_books.remove if seen_by == user.id
    # selected_genres = '-'.join(selected_genres)
    genre_objs = []
    for i in selected_genres:
        genre_objs.append(Genre.objects.get(id=i))
    selected_genres = '-'.join(selected_genres)
    if display_books.exists():
        total_books = len(display_books)
        p_n = Paginator(display_books, 1)
        page = request.GET.get('page')
        pages = p_n.get_page(page)
        return render(request, 'synopsis/synopsis.html',
                      {'pages': pages, 'selected_genres': selected_genres, 'total_books': total_books, 'genre_objs': genre_objs, 'member': member})
    else:
        messages.success(
            request, 'We couldnt find anything to match your search. Try reseting synopsis in Account Info to see books again.')
        return render(request, 'synopsis/synopsis.html')


def book_info(request, book_id):
    ''' if the user clicks the synopsis of a book in the paginated synopsis
    app they will be taken to a page showing more information about the
    book from the book object.
    The user is also given the option to add the book to their mybooks
    list or remove it depending on the current status oif the book
    '''
    book = Book.objects.get(pk=book_id)
    liked = False
    if book.liked_by.filter(id=request.user.id).exists():
        liked = True
    return render(request, 'synopsis/book_info.html', {'book': book, 'liked': liked, })


def like_view(request, id):
    referer = request.META.get('HTTP_REFERER')
    referer = referer.split('/')
    selected_genres = referer[-1].partition('?')[0]

    '''liked view is a templateless function that provids
    the liked_by functionality.
    when the like button is clicked the function is called
    and the appropriate chenges are made to the member model,
    the page is then reversed back to the book info page
    '''
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
    if referer[-2] == "synopsis":

        print(selected_genres)
        return redirect(synopsis, selected_genres)
    else:
        return HttpResponseRedirect(reverse('book_info', kwargs={'book_id': book_id}))


def my_books(request):
    ''' My books searchs the book model for anybooks where the
    logged in user liked_by field is set to true,
    the results are then shown to the user with various options.
    '''
    if request.user.is_authenticated:
        my_books = Book.objects.filter(
            liked_by=request.user.id)
        return render(request, 'synopsis/my_books.html', {'my_books': my_books})
    else:
        messages.success(request, (
            "You must be logged in to view this page"))
        return redirect('home')


def search_book(request):
    '''This is an admin only function that allows the logged in user
    to search for a book which can bew subsiquently deleted or updated.
    '''
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
    '''an admin only function in response to a search the user
    can update any information aboout a book using the update form.
    '''
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
    '''an admin only function in response to a search the user
    can delete any a book.
    '''
    book_to_delete = get_object_or_404(Book, id=book_id)
    delete_title = book_to_delete.title
    book_to_delete.delete()
    messages.success(
        request, (f'{delete_title} has been deleted.'))
    return redirect('search_book')


def remove_book(request, book_id):
    ''' remove like if the user clicks the button remove the like from th
    book object and reload the page.
    Works in the same way as the like funtion on the like view
    however only give the option to remove from the list '''
    book = get_object_or_404(Book, id=book_id)
    member = request.user.member
    member.liked_books.remove(book.id)
    book.liked_by.remove(request.user.id)
    liked = False
    return HttpResponseRedirect(reverse('my_books'))


def the_last_page(request, selected_genres):
    selected_genres = selected_genres.split('-')
    print(selected_genres)
    genre_objs = []
    for i in selected_genres:
        genre_objs.append(Genre.objects.get(id=i))
    return render(request, 'synopsis/the_last_page.html', {'genre_objs': genre_objs})
