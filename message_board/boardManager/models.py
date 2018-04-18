from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User

import uuid
import base64
import hashlib
import os


def shortUUID():
    return ascii(base64.urlsafe_b64encode(hashlib.sha256(os.urandom(128)).digest()))[2:10]


def mediumUUID():
    return ascii(base64.urlsafe_b64encode(hashlib.sha256(os.urandom(128)).digest()))[2:34]


# Create your models here.


def upload_path(instance, filename):
    return '{0}/{1}'.format(instance.comment.creator.username, filename)


class Forum(models.Model):
    id = models.CharField(
        max_length=8, primary_key=True, default=shortUUID, editable=False)
    name = models.CharField(max_length=200, unique=True)
    create_date_time = models.DateTimeField(
        default=timezone.now, editable=False)
    thread_count = models.IntegerField(default=0)
    admins = models.ManyToManyField(
        User, limit_choices_to={'is_staff': True}, blank = True)

    def __str__(self):
        return self.name


class Thread(models.Model):
    id = models.CharField(
        max_length=8, primary_key=True, default=shortUUID, editable=False)
    name = models.CharField(max_length=200)
    create_date_time = models.DateTimeField(default=timezone.now, editable=False)
    forum = models.name = models.ForeignKey(
        Forum, to_field='name', related_name='threads', on_delete=models.CASCADE)
    comment_count = models.IntegerField(default=0)
    creator = models.ForeignKey(
        User, to_field='username', related_name='threads', on_delete=models.SET_DEFAULT, default='[deleted]')

    def __str__(self):
        return 'ID: {0} Name: {1} Creator: {2}'.format(self.id, self.name, self.creator)


class Comment(models.Model):
    id = models.CharField(
        max_length=32, primary_key=True, default=mediumUUID, editable=False)
    create_date_time = models.DateTimeField(
        default=timezone.now, editable=False)
    contents = models.TextField()
    creator = models.ForeignKey(
        User, to_field='username', related_name='comments', on_delete=models.SET_DEFAULT, default='[deleted]')
    thread = models.ForeignKey(
        Thread, to_field='id', related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return 'ID: {0} Creator: {1} Contents: {2} Created: {3}'.format(self.id, self.creator, self.contents, self.create_date_time)


class Attachment(models.Model):
    comment = models.ForeignKey(
        Comment, to_field='id', related_name='attachments', on_delete=models.CASCADE)
    file = models.FileField(upload_to=upload_path, max_length=200)

    def __str__(self):
        return '{}'.format(self.file)


class Tag(models.Model):
    tag_name = models.CharField(max_length=30, unique = True)
    tagged_threads = models.ManyToManyField(to='Thread', blank=True)

    def __str__(self):
        return '{}'.format(self.tag_name)


@receiver(post_save, sender=Thread)
def update_thread_count(sender, **kwargs):
    if kwargs.get('created', True):
        a = kwargs.get('instance')
        a.forum.thread_count = Thread.objects.filter(forum__exact = a.forum).count()
        a.save()
        a.forum.save()
        print('incremented thread count for forum {0}'.format(a.forum.name))


@receiver(post_save, sender=Comment)
def update_comment_count(sender, **kwargs):
    if kwargs.get('created', True):
        a = kwargs.get('instance')
        a.thread.comment_count = Comment.objects.filter(thread__exact = a.thread).count()
        a.save()
        a.thread.save()
        print('incremented comment count for thread {0}'.format(a.thread.name))
