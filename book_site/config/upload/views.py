from django.shortcuts import render

# Create your views here.


def mass_upload(request):
    return render(request, 'upload/upload.html')
