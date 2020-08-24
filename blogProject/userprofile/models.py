from django.db import models
from django.contrib.auth.models import User
import time


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatar/%Y%m%d/', blank=True)
    bio = models.TextField(max_length=500, blank=True)
    real_name = models.CharField(max_length=20)
    email = models.CharField(max_length=20)
    profession = models.CharField(max_length=20)
    english_level =  models.CharField(max_length=20,blank=True)
    location =  models.CharField(max_length=20,blank=True)
    nationality =  models.CharField(max_length=20,blank=True)
    skill1 =  models.CharField(max_length=30,blank=True)
    skill2 = models.CharField(max_length=30, blank=True)
    skill3 = models.CharField(max_length=30, blank=True)
    skill4 = models.CharField(max_length=30, blank=True)
    skill5 = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return 'user {}'.format(self.user.username)


class ResumePersonalInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=200, blank=True)
    avatar = models.ImageField(upload_to='avatar/%Y%m%d/', blank=True)
    address = models.CharField(max_length=300, blank=True)
    real_name = models.CharField(max_length=200)
    website = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    current_status = models.CharField(max_length=200)  # the description under the name
    linkedin = models.URLField(blank=True)
    github = models.URLField(blank=True)

    class Meta:
        verbose_name_plural = "Personal Info"


class ResumeEducation(models.Model):
    name = models.CharField(max_length=250)
    programme = models.CharField(max_length=250)
    start_date = models.DateField()
    completion_date = models.DateField()
    summary = models.TextField()
    is_current = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Education"


class ResumeJob(models.Model):
    company = models.CharField(max_length=250)
    location = models.CharField(max_length=250)
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    completion_date = models.DateField()
    is_current = models.BooleanField(default=False)
    is_public = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Job"
        ordering = ['-completion_date', '-start_date']


class ResumeReserach(models.Model):
    name = models.CharField(max_length=250)
    location = models.CharField(max_length=250)
    start_date = models.DateField()
    completion_date = models.DateField()
    summary = models.TextField()

    class Meta:
        verbose_name_plural = "Research"


class ResumeSkillset(models.Model):
    name = models.CharField(max_length=250)

    class Meta:
        verbose_name_plural = "Skill"


class Skill(models.Model):
    name = models.CharField(max_length=250)
    skillset = models.ForeignKey('ResumeSkillset', on_delete=models.CASCADE)

    class Meta:
        ordering = ['id']

    def __unicode__(self):
        return ''.join([self.skillset.name, '-', self.name])