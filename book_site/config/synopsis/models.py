from django.db import models
from members.models import User

# greres calsses used to catagorise book entries


class Genre(models.Model):
    genre = models.CharField(
        'Genre', default='Adventure', max_length=10, unique=True)

    def __str__(self):
        return self.genre


class Book(models.Model):
    title = models.CharField('Title', max_length=25)
    author = models.CharField('Author', max_length=25)
    publish_date = models.DateField('Date Publised',)
    synopsis = models.TextField('Synopsis', max_length=2200)
    genre = models.ForeignKey(
        Genre, on_delete=models.SET_DEFAULT, default='Adventure')
    purchase_link = models.URLField('Link to Purchase',)
    liked_by = models.ManyToManyField(
        User,  symmetrical=False, blank=True, related_name='liked_by')
    seen_by = models.ManyToManyField(
        User,  symmetrical=False, blank=True, related_name='seen_by')

    def __str__(self):
        return self.title
