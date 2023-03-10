from django import forms
from .models import csv_file


class upload_form(forms.ModelForm):
    file_name = forms.FileField(
        label='Upload CSV file.',
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = csv_file
        fields = ('file_name',)
