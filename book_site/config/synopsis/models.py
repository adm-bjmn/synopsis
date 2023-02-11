from django.db import models

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

    def __str__(self):
        return self.title

# additional members class to use with djangos User class


class Member(models.Model):
    first_name = models.CharField('First Name', max_length=25)
    last_name = models.CharField('Last Name', max_length=25)
    email = models.EmailField('Email', max_length=25)
    liked_books = models.ManyToManyField(Book, blank=True)

    def __str__(self):
        return self.first_name, self.last_name
