from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('synopsis/<selected_genres>', views.synopsis, name='synopsis'),
    path('book_info/<book_id>', views.book_info, name='book_info'),
    path('like_book/<int:id>',
         views.like_view, name='like_book'),

    path('my_books', views.my_books, name='my_books'),
    path('remove_book/<book_id>', views.remove_book, name='remove_book'),
    path('search_book/', views.search_book, name='search_book'),
    path('update_book/<book_id>', views.update_book, name='update_book'),
    path('delete_book/<book_id>', views.delete_book, name='delete_book'),

]
