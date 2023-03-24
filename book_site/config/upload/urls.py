from . import views
from django.urls import path

urlpatterns = [
    path('backup', views.backup_via_csv, name='backup'),
    path('', views.upload_by_scrape, name='upload'),
]
