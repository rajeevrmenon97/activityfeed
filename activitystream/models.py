from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class Post(models.Model):
    content = models.TextField(blank=False)
    user = models.ForeignKey(User, blank=False, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    user = models.ForeignKey(User, blank=False, on_delete=models.CASCADE)
    content = models.TextField(blank=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)

class Upvote(models.Model):
    user = models.ForeignKey(User, blank=False, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

class Activity(models.Model):
    actor = models.ForeignKey(User, blank=False, on_delete=models.CASCADE)

    class Verb(models.TextChoices):
        POST = 'PST', _('Post')
        COMMENT = 'CMT', _('Comment')
        UPVOTE = 'UVT', _('Upvote')

    verb = models.CharField(max_length=3, choices=Verb.choices, blank=False)
    comment = models.ForeignKey(Comment, default=None, blank=True, null=True, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, default=None, blank=True, null=True, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

class Following(models.Model):
    user = models.ForeignKey(User, related_name='baseuser', blank=False, on_delete=models.CASCADE)
    target_user = models.ForeignKey(User, related_name='targeruser', blank=False, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

class Feed(models.Model):
    user = models.ForeignKey(User, blank=False, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, default=None, blank=True, null=True, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
