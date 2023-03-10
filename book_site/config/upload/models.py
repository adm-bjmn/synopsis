from django.db import models

# Create your models here.


class csv_file(models.Model):
    file_name = models.FileField(upload_to='csv_files')
    upload_date = models.DateField(auto_now_add=True)
    file_processed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.upload_date)
