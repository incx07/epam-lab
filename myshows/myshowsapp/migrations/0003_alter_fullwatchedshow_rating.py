# Generated by Django 3.2.3 on 2021-07-15 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myshowsapp', '0002_auto_20210616_2002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fullwatchedshow',
            name='rating',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], default='No', max_length=2),
        ),
    ]
