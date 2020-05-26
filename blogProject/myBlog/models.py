# -*- coding: utf-8 -*-
from django.contrib.auth.models import AbstractUser, User
from django.db import models


# Profile Model
# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
#     phone = models.CharField(max_length=20, blank=True)
#     avatar = models.ImageField(upload_to='avatar/%Y%m%d/', blank=True)
#     bio = models.TextField(max_length=500, blank=True)
#
#     class Meta:
#         verbose_name = 'Profile'
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return 'user {}'.format(self.user.username)


# Tag Model
class Tag(models.Model):
    name = models.CharField(max_length=20, verbose_name='标签名称')

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# Category Model
class Category(models.Model):
    name = models.CharField(max_length=30, verbose_name='标签分类')
    index = models.IntegerField(default=999, verbose_name='分类的排序')

    class Meta:
        verbose_name = 'Categories'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# Article Model
class Article(models.Model):
    title = models.CharField(max_length=50, verbose_name="Title")
    desc = models.CharField(max_length=50, verbose_name="Description")
    content = models.TextField(verbose_name="Content")
    total_views = models.PositiveIntegerField(default=0,verbose_name="views")
    likes = models.PositiveIntegerField(default=0)
    # click_count = models.IntegerField(default=0, verbose_name="C")
    is_recommend = models.BooleanField(default=False, verbose_name="Do you want to recommend this article?")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='Create time')
    last_modified_time = models.DateTimeField(auto_now=True, verbose_name='Last modified time')
    author = models.ForeignKey(User, blank=True, null=True,verbose_name="Author", on_delete=models.CASCADE)
    category = models.ForeignKey(Category, blank=True, null=True, verbose_name="Category",on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag, verbose_name="tag")

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = verbose_name
        ordering = ['-last_modified_time']

        def __str__(self):
            return self.title


# Comment Model
class Comment(models.Model):
    content = models.TextField(verbose_name='评论内容')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    views = models.PositiveIntegerField('浏览量', default=0)
    likes = models.PositiveIntegerField('点赞数', default=0)
    abstract = models.CharField(max_length=54, blank=True, null=True, verbose_name="文章摘要")
    topped = models.BooleanField('置顶', default=False)
    user = models.ForeignKey(User, blank=True, null=True, verbose_name='用户',on_delete=models.CASCADE)
    article = models.ForeignKey(Article, blank=True, null=True, verbose_name='文章',on_delete=models.CASCADE)
    pid = models.ForeignKey('self', blank=True, null=True, verbose_name='父级评论',on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Comments"
        verbose_name_plural = verbose_name
        ordering = ['-created_time']

        def __str__(self):
            return str(self.id)


# Links Model
class Links(models.Model):
    title = models.CharField(max_length=50, verbose_name='标题')
    desc = models.CharField(max_length=20, verbose_name='友情链接描述')
    callback_url = models.URLField(verbose_name="URL地址")
    date_publish = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    index = models.IntegerField(default=999, verbose_name='排列顺序从大到小')

    class Meta:
        verbose_name = "Linking"
        verbose_name_plural = verbose_name
        ordering = ['index', 'id']

        def __str__(self):
            return self.title


# Advertising Model
class Advertising(models.Model):
    title = models.CharField(max_length=50, verbose_name='广告标题')
    desc = models.CharField(max_length=200, verbose_name='广告描述')
    image_url = models.ImageField(upload_to='ad/%Y/%m', verbose_name='图片路径')
    callback_url = models.URLField(null=True, blank=True, verbose_name='回调url')
    date_publish = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    index = models.IntegerField(default=999, verbose_name='排列顺序从大到小')

    class Meta:
        verbose_name = "Ad"
        verbose_name_plural = verbose_name
        ordering = ['index', 'id']

        def __str__(self):
            return self.title
