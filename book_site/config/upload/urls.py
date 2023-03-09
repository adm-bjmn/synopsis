from . import views
from django.urls import path

urlpatterns = [
    path('', views.mass_upload, name='upload'),
]
