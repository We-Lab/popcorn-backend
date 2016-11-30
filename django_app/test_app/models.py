from django.db import models

from mysite import settings


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=30)
    context = models.TextField()