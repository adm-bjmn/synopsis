# Generated by Django 4.1.3 on 2023-03-10 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='csv_file',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.FileField(upload_to='csv_files')),
                ('upload_date', models.DateField(auto_now_add=True)),
                ('file_processed', models.BooleanField(default=False)),
            ],
        ),
    ]