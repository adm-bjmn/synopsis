# Generated by Django 4.1.3 on 2023-03-23 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('synopsis', '0010_book_genre'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='img_link',
            field=models.URLField(default='www.imageURL.not', verbose_name='Image Link'),
            preserve_default=False,
        ),
    ]
