# Generated by Django 3.0.6 on 2020-05-26 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0002_auto_20200526_1546'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='email',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profession',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='profile',
            name='real_name',
            field=models.CharField(max_length=20),
        ),
    ]
