# -*- encoding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models


class Jornada(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    photo = models.URLField(null=True, blank=True)

    def __unicode__(self):
        return self.title


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    jornada = models.ForeignKey(Jornada, on_delete=models.CASCADE)
    text = models.TextField()
    url = models.URLField(null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.jornada.title +' - '+ self.author.username +' - '+ str(self.create_at)

