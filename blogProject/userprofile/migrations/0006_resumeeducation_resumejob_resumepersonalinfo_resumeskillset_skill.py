# Generated by Django 3.0.6 on 2020-08-19 05:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('userprofile', '0005_auto_20200527_1739'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResumeEducation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('location', models.CharField(max_length=250)),
                ('start_date', models.DateField()),
                ('completion_date', models.DateField()),
                ('summary', models.TextField()),
                ('is_current', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'Education',
            },
        ),
        migrations.CreateModel(
            name='ResumeJob',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(max_length=250)),
                ('location', models.CharField(max_length=250)),
                ('title', models.CharField(max_length=250)),
                ('description', models.TextField(blank=True)),
                ('start_date', models.DateField()),
                ('completion_date', models.DateField()),
                ('is_current', models.BooleanField(default=False)),
                ('is_public', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'Job',
                'ordering': ['-completion_date', '-start_date'],
            },
        ),
        migrations.CreateModel(
            name='ResumeSkillset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('skillset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userprofile.ResumeSkillset')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='ResumePersonalInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('avatar', models.ImageField(blank=True, upload_to='avatar/%Y%m%d/')),
                ('address', models.CharField(blank=True, max_length=100)),
                ('real_name', models.CharField(max_length=20)),
                ('website', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=20)),
                ('current_status', models.CharField(max_length=100)),
                ('linkedin', models.URLField(blank=True)),
                ('github', models.URLField(blank=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Personal Info',
            },
        ),
    ]
