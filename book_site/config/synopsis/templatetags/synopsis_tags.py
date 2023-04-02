from django import template
from django.shortcuts import get_object_or_404
from synopsis.models import Book
from members.models import User

register = template.Library()


@register.simple_tag
def test_tag(book_id, user_id):
    book = get_object_or_404(Book, id=book_id)
    user = get_object_or_404(User, id=user_id)
    book.seen_by.add(user)
    print(f'Kowabunga {book_id} : {user_id}')
    return ''
