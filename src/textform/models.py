# coding: utf-8

from __future__ import unicode_literals
import datetime
from django.utils import timezone
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User
from login.models import UserProfile
from blogs.models import Blog

@python_2_unicode_compatible
class Message(models.Model):
    title = models.CharField(max_length=100, verbose_name=u'Заголовок поста', default='none')
    text = models.TextField(verbose_name=u'Текст поста')
    author = models.ForeignKey(User, null=True, blank=True, verbose_name=u'Автор поста')

    answer_count = models.IntegerField(null=True, blank=True, verbose_name=u'Количество комментариев')
    like_count = models.IntegerField(null=True, blank=True, verbose_name=u'Количество лайков')

    pub_date = models.DateTimeField(verbose_name=u'Дата создания поста', auto_now_add=True)
    mod_date = models.DateTimeField(verbose_name=u'Дата последней модификации', auto_now=True)

    blog = models.ForeignKey(Blog, null=True, blank=True, verbose_name=u'Блог', on_delete=models.CASCADE)

    published = models.BooleanField(default=True)
	
    def __str__(self):
        return self.text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def message_beginning(self):
        return self.text[:150]


