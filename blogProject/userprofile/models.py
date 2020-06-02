from django.db import models
from django.contrib.auth.models import User


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
