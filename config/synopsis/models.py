from django.db import models
from members.models import User

# greres calsses used to catagorise book entries


class Genre(models.Model):
    ''' The Genre model allows Genre objects to be created which can
    then be associated to a book object via a many to many field.
    Each book can have an number of genres 
    associated to it. including None.
    '''
    genre = models.CharField(
        'Genre', default='adventure', max_length=25, unique=True)
    ght = models.CharField(
        'Genre Human Text', default='Adventure', max_length=25, unique=True)

    def __str__(self):
        return self.ght


class Book(models.Model):
    ''' The book model provides the main object for the synopsis functionality
    Aside from the Obvious critera for a book, the model also includes
    a link to an image online and a link to a destination where 
    the book can be purchased.
    The many to many fields liked_by and seen_by are functionality fields.
    A book that has been liked by a user will apear in thier my books page,
    while a book that has been seen_by a user will not appear in future
    searches unless seen_by is reset on the profile page.
    '''
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
