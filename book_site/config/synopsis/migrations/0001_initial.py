# Generated by Django 4.1.3 on 2023-02-11 17:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre', models.CharField(default='Adventure', max_length=10, verbose_name='Genre')),
            ],
        ),
        migrations.CreateModel(
            name='Members',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=25, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=25, verbose_name='Last Name')),
                ('email', models.EmailField(max_length=25, verbose_name='Email')),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=25, verbose_name='Title')),
                ('author', models.CharField(max_length=25, verbose_name='Author')),
                ('publish_date', models.DateField(verbose_name='Date Publised')),
                ('synopsis', models.TextField(max_length=2200, verbose_name='Synopsis')),
                ('purchase_link', models.URLField(verbose_name='Link to Purchase')),
                ('genre', models.ForeignKey(default='Adventure', on_delete=django.db.models.deletion.SET_DEFAULT, to='synopsis.genre')),
                ('liked_by', models.ManyToManyField(blank=True, to='synopsis.members')),
            ],
        ),
    ]
