from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('synopsis/', views.dashboard, name='dashboard'),
    # path('synopsis/', views.synopsis, name='synopsis')
    # path('book_info/<pk>')
]
