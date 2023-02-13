from django import forms
from .models import Genre


class BlankForm():
    blank = forms.CharField()

    class Meta:
        model = Genre
        fields = ()
