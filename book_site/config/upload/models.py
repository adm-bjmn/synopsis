from django.db import models

# Create your models here.


class csv_file(models.Model):
    ''' CSV file is a model created to collect the CSV forms 
    generated when the update database function is called.
    '''
    file_name = models.FileField(upload_to='csv_files')
    upload_date = models.DateField(auto_now_add=True)
    file_processed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.upload_date)
