# Generated by Django 4.1.3 on 2023-02-11 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('synopsis', '0002_rename_members_member'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='liked_by',
        ),
        migrations.AddField(
            model_name='member',
            name='liked_books',
            field=models.ManyToManyField(blank=True, to='synopsis.book'),
        ),
    ]
