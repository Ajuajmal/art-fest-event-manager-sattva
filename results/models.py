from __future__ import unicode_literals
from django.db import models
from django import forms
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone
import os
from django.core.validators import RegexValidator
from django.contrib.postgres.fields import JSONField
from django.utils.safestring import mark_safe


from events.models import Participant, Event


BRANCH = (
    (0, "CE"),
    (1, "CS"),
    (2, "EC"),
    (3, "EEE"),
    (4, "IT"),
    (5, "ME"),
    (6, "MCA")
)




SEM = (
    (1, "S2"),
    (3, "S4"),
    (5, "S6"),
    (7, "S8"),
    (8, "Semester"),
)


POS = (
    (1, "FIRST"),
    (2, "SECOND"),
    (3, "THIRD"),
    (4, "OTHER"),
)

class BranchPoint(models.Model):
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True)
    branch = models.IntegerField(choices=BRANCH, default=0)
    position = models.IntegerField(choices=POS, default=4)
    score = models.IntegerField()
    updated_on = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['updated_on']
    def publish(self):
        self.updated_on = timezone.now()
        self.save()

    def __str__(self):
        return '%s' % (self.event)
class EventsResult(models.Model):
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True)

    winners = RichTextField(blank=True)

    updated_on = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-updated_on']
    def publish(self):
        self.updated_on = timezone.now()
        self.save()

    def __str__(self):
        return '%s' % (self.event)
