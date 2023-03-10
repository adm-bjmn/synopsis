from django.shortcuts import render
from .forms import upload_form
from .models import csv_file
import csv
from synopsis.models import Book
# Create your views here.


def mass_upload(request):
    form = upload_form(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(
            request, ('Form successfully uoploaded'))
        form = upload_form()
        new_file = csv_file.objects.get(processed=False)
        # add in a try loop here for bad file uploads
        with open(new_file.file_name.path, 'r') as f:
            new_releases = csv.reader(f)
            for rows in new_releases:
                print(rows)
                # next step is to clean the input from the csv and make use
                # it is a well presented list ready for slcing
                # then the slices can be used to create a new book object.
                title = rows[1]
                author = rows[2]
                publish_date = rows[3]
                synopsis = rows[4]
                genre = rows[5]
                purchase_link = rows[6]
                Book.objects.create(
                    title=title,
                    author=author,
                    publish_date=publish_date,
                    synopsis=synopsis,
                    genre=genre,
                    purchase_link=purchase_link,
                )
        # once the file has been processed the proceessed check box is marked automatically
        # to ensure the file is not picked up next time an upload is commited.
        new_file.processed = True
        new_file.save()
    return render(request, 'upload/upload.html', {'form': form, })
