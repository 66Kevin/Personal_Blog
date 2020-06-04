# -*- coding: utf-8 -*-
from django.contrib.auth.models import AbstractUser, User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from PIL import Image


# Tag Model
class Tag(models.Model):
    name = models.CharField(max_length=20, verbose_name='标签名称')

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Category(models.Model):
    title = models.CharField(max_length=100, blank=True)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


# Article Model
class Article(models.Model):
    title = models.CharField(max_length=50, verbose_name="Title")
    desc = models.CharField(max_length=50, verbose_name="Description")
    avatar = models.ImageField(upload_to='article/%Y%m%d/', blank=True)
    content = models.TextField(verbose_name="Content")
    total_views = models.PositiveIntegerField(default=0, verbose_name="views")
    likes = models.PositiveIntegerField(default=0)
    # click_count = models.IntegerField(default=0, verbose_name="C")
    is_recommend = models.BooleanField(default=False, verbose_name="Do you want to recommend this article?")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='Create time')
    last_modified_time = models.DateTimeField(auto_now=True, verbose_name='Last modified time')
    author = models.ForeignKey(User, blank=True, null=True, verbose_name="Author", on_delete=models.CASCADE)
    # category = models.ForeignKey(Category, blank=True, null=True, verbose_name="Category", on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag, verbose_name="tag")
    column = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='article'
    )

    def get_absolute_url(self):
        return reverse('myBlog:article_detail', args=[self.id])

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = verbose_name
        ordering = ['-last_modified_time']

        def __str__(self):
            return self.title

    # 保存时处理图片
    def save(self, *args, **kwargs):
        # 调用原有的 save() 的功能
        article = super(Article, self).save(*args, **kwargs)

        # 固定宽度缩放图片大小
        if self.avatar and not kwargs.get('update_fields'):
            image = Image.open(self.avatar)
            (x, y) = image.size
            new_x = 400
            new_y = int(new_x * (y / x))
            resized_image = image.resize((new_x, new_y), Image.ANTIALIAS)
            resized_image.save(self.avatar.path)

        return article


# Comment Model
class Comment(models.Model):
    content = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, blank=True, null=True, verbose_name='user', on_delete=models.CASCADE)
    article = models.ForeignKey(Article, blank=True, null=True, verbose_name='article', on_delete=models.CASCADE)
    pid = models.ForeignKey('self', blank=True, null=True, verbose_name='parent comment', on_delete=models.CASCADE)

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
