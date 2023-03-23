from django.db import models
from members.models import User

# greres calsses used to catagorise book entries


class Genre(models.Model):
    genre = models.CharField(
        'Genre', default='adventure', max_length=25, unique=True)
    ght = models.CharField(
        'Genre Human Text', default='Adventure', max_length=25, unique=True)

    def __str__(self):
        return self.ght


class Book(models.Model):
    title = models.CharField('Title', max_length=25)
    author = models.CharField('Author', max_length=25)
    publish_date = models.DateField('Date Publised',)
    synopsis = models.TextField('Synopsis', max_length=2200)
    genre = models.ManyToManyField(
        Genre, symmetrical=False, blank=True, related_name='genre_list')
    purchase_link = models.URLField('Link to Purchase',)
    img_link = models.URLField('Image Link',)
    liked_by = models.ManyToManyField(
        User,  symmetrical=False, blank=True, related_name='liked_by')
    seen_by = models.ManyToManyField(
        User,  symmetrical=False, blank=True, related_name='seen_by')

    def __str__(self):
        return self.title
