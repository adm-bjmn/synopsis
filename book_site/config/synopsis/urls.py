from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('synopsis/<genre_id>', views.synopsis, name='synopsis'),
    path('book_info/<book_id>', views.book_info, name='book_info'),
    path('like_book/<int:id>',
         views.like_view, name='like_book'),
    path('my_books', views.my_books, name='my_books'),
    path('profile/', views.user_profile, name='user_profile')
]
