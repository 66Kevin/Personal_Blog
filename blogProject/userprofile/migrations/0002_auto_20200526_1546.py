# Generated by Django 3.0.6 on 2020-05-26 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='email',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='profile',
            name='english_level',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='profile',
            name='location',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='profile',
            name='nationality',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='profile',
            name='profession',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='profile',
            name='real_name',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='profile',
            name='skill1',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AddField(
            model_name='profile',
            name='skill2',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AddField(
            model_name='profile',
            name='skill3',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AddField(
            model_name='profile',
            name='skill4',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AddField(
            model_name='profile',
            name='skill5',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]
