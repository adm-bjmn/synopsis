from django import template
from django.shortcuts import get_object_or_404
from synopsis.models import Book
from members.models import User

register = template.Library()

book_list = []


@register.simple_tag
def test_tag(book_id, user_id):
    book = get_object_or_404(Book, id=book_id)
    user = get_object_or_404(User, id=user_id)
    book_list.append(book)
    # book.seen_by.add(user)
    print(f'Kowabunga {book_list}')
    return ''


@register.simple_tag
def seen_by_tag(user_id):
    global book_list
    user = get_object_or_404(User, id=user_id)
    for book in book_list:
        book.seen_by.add(user)
    book_list = []
    print('I did it!')
    return ''
