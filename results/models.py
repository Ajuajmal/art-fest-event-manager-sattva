from __future__ import unicode_literals
from django.db import models
from django import forms
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone
import os
from django.core.validators import RegexValidator

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

class BranchPoint(models.Model):
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True)
    branch = models.IntegerField(choices=BRANCH, default=0)
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
    winner11 = models.ForeignKey(Participant,on_delete=models.SET_NULL, null=True,blank=True, default=None, related_name='related_winner11')
    winnerbranch11 = models.CharField(max_length=200,null=True,blank=True, default=None,help_text='WARNING : Use this field when no data found about participant')
    winner12 = models.ForeignKey(Participant,on_delete=models.SET_NULL, null=True,blank=True, default=None, related_name='related_winner12')
    winner13 = models.ForeignKey(Participant,on_delete=models.SET_NULL, null=True,blank=True, default=None, related_name='related_winner13')
    winner14 = models.ForeignKey(Participant,on_delete=models.SET_NULL, null=True,blank=True, default=None, related_name='related_winner14')
    winner21 = models.ForeignKey(Participant,on_delete=models.SET_NULL, null=True,blank=True, default=None, related_name='related_winner21')
    winnerbranch21 = models.CharField(max_length=200,null=True,blank=True, default=None,help_text='WARNING : Use this field when no data found about participant')
    winner22 = models.ForeignKey(Participant,on_delete=models.SET_NULL, null=True,blank=True, default=None, related_name='related_winner22')
    winner23 = models.ForeignKey(Participant,on_delete=models.SET_NULL, null=True,blank=True, default=None, related_name='related_winner23')
    winner24 = models.ForeignKey(Participant,on_delete=models.SET_NULL, null=True,blank=True, default=None, related_name='related_winner24')
    winner31 = models.ForeignKey(Participant,on_delete=models.SET_NULL, null=True,blank=True, default=None, related_name='related_winner31')
    winnerbranch31 = models.CharField(max_length=200,null=True,blank=True, default=None,help_text='WARNING : Use this field when no data found about participant')
    winner32 = models.ForeignKey(Participant,on_delete=models.SET_NULL, null=True,blank=True, default=None, related_name='related_winner32')
    winner33 = models.ForeignKey(Participant,on_delete=models.SET_NULL, null=True,blank=True, default=None, related_name='related_winner33')
    winner34 = models.ForeignKey(Participant,on_delete=models.SET_NULL, null=True,blank=True, default=None, related_name='related_winner34')

    updated_on = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-updated_on']
    def publish(self):
        self.updated_on = timezone.now()
        self.save()

    def __str__(self):
        return '%s' % (self.event)
