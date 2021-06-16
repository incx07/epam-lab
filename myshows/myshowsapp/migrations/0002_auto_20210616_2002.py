# Generated by Django 3.2.3 on 2021-06-16 20:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myshowsapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FullWatchedShow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('myshows_id', models.PositiveIntegerField(default=0)),
                ('title_eng', models.CharField(max_length=100)),
                ('year', models.PositiveSmallIntegerField(default=0)),
                ('rating', models.CharField(default='No', max_length=5)),
                ('user_link', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LaterWatchShow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('myshows_id', models.PositiveIntegerField(default=0)),
                ('title_eng', models.CharField(max_length=100)),
                ('year', models.PositiveSmallIntegerField(default=0)),
                ('user_link', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='showtowatch',
            name='user_link',
        ),
        migrations.DeleteModel(
            name='ShowFullWatched',
        ),
        migrations.DeleteModel(
            name='ShowToWatch',
        ),
    ]
