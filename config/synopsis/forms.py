from django import forms
from .models import Genre, Book
from django.forms import ModelForm

# ======= UNUSED FROM ==============
'''THis form was generatred in the early stages of development as a
way to slect genres via multiple choice in the sdashboard view
however I prefered to style the checkboxes myself and so opted 
to use a loop and get the genre objects instead and give each 
checkbox a values fto be processd in the view rather than by a form
'''


class GenreForm(forms.Form):
    ''' The genre form is used on the dashboard view to present the user with 
    the option to select any number of genres to be used as search criteria 
    for the main synopsis functionality. The form is a multiple choice form
    with check boxes.
    '''
    genre_choices = []
    for i in Genre.objects.all():
        genre_choices.append((i.id, i.genre))

    selected_genres = forms.MultipleChoiceField(
        label='',
        choices=tuple(genre_choices),
        widget=forms.CheckboxSelectMultiple())


class UpdateBookForm(ModelForm):
    ''' Update book is an admin only function that allows admin to update 
    information or broken links on a book object.
    the from presented after a search function and displays the 
    book object with its information in form fields ready to be changed.
    '''
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
    genre = forms.ModelChoiceField(queryset=Genre.objects.all(),  # needs to be multiple choise
                                   label='Genre',
                                   widget=forms.Select(
                                       attrs={'class': 'form-control'})
                                   )
#  add links to form

    class Meta:
        model = Book
        fields = ('title', 'author', 'synopsis', 'genre',)
