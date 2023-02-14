from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('synopsis/<genre_id>', views.synopsis, name='synopsis'),
    path('book_info/<book_id>', views.book_info, name='book_info'),
]
