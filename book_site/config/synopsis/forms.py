from django import forms
from .models import Genre, Book
from django.forms import ModelForm


class BlankForm():
    blank = forms.CharField()

    class Meta:
        model = Genre
        fields = ()


class UpdateBookForm(ModelForm):
    title = forms.CharField(
        label='Title',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    author = forms.CharField(
        label='Author',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    synopsis = forms.CharField(
        label='Synopsis',
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )
    genre = forms.ModelChoiceField(queryset=Genre.objects.all(),
                                   label='Genre',
                                   widget=forms.Select(
                                       attrs={'class': 'form-control'})
                                   )

    class Meta:
        model = Book
        fields = ('title', 'author', 'synopsis', 'genre',)


'''    title = models.CharField('Title', max_length=25)
    author = models.CharField('Author', max_length=25)
    publish_date = models.DateField('Date Publised',)
    synopsis = models.TextField('Synopsis', max_length=2200)
    genre = models.ForeignKey(
        Genre, on_delete=models.SET_DEFAULT, default='Adventure')
    purchase_link = models.URLField('Link to Purchase',)
    liked_by = models.ManyToManyField(
        User,  symmetrical=False, blank=True, related_name='liked_by')
    seen_by = models.ManyToManyField(
        User,  symmetrical=False, blank=True, related_name='seen_by')'''
