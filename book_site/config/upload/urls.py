from . import views
from django.urls import path

urlpatterns = [
    # path('', views.upload_by_csv, name='upload'),
    path('', views.upload_by_scrape, name='upload'),
]
