from django import forms
from .models import csv_file

# curently unused form.


class upload_form(forms.ModelForm):
    ''' The CSV model is file form that recieves a CSV file when
    the data base is uploaded. This file can then be accessed by 
    admin for the purpose of data analysis or other such activities.
    Tihis from can be used to upload a file manually should you wish,
    without having to update the whole database.
    '''
    file_name = forms.FileField(
        label='Upload CSV file.',
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = csv_file
        fields = ('file_name',)
