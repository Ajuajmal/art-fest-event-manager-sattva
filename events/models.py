from django.db import models
from django import forms
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone
import os
from django.core.validators import RegexValidator


def user_directory_path(instance, filename):
    basefilename, file_extension = os.path.splitext(filename)
    timenow = timezone.now()
    return 'events/{userid}/{date}{basename}{time}{ext}'.format(userid=instance.scheduler.id, basename=basefilename, date=timenow.strftime("%Y%m%d"), time=timenow.strftime("%H%M%S"), ext=file_extension)

VENUE = (
    (0,"Scheduled"),
    (1,"Draft"),
    (2,"Withdrawn"),
    (3, "Stage 1"),
    (4, "Stage 2"),
    (5, "Stage 3"),
    (6, "Stage 4"),
    (7, "Stage 5"),
    (8, "Stage 6"),
)

EVENTTYPE = (
    (0,"Individual"),
    (1,"Group"),
)
class Category(models.Model):
    name = models.CharField(max_length=50,default='None')
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['-name']
    def __str__(self):
        return self.name

class Event(models.Model):
    category = models.ForeignKey(Category,on_delete=models.SET_NULL, null=True)
    scheduler = models.ForeignKey(User, on_delete= models.CASCADE, related_name="event_auth")
    name = models.CharField(max_length=200)
    eventtype = models.IntegerField(choices=EVENTTYPE, default=0)
    date = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField(default=timezone.now)
    venue = models.IntegerField(choices=VENUE, default=1)
    cover = models.ImageField(upload_to=user_directory_path, default='defaultevent.jpg')
    about = RichTextUploadingField()
    max_participants = models.IntegerField(default=0)
    slug = models.SlugField(max_length=200, unique=True, help_text='WARNING : Use the same slug for while creating a Terms about events')

    class Meta:
        verbose_name_plural = "Events"
        ordering = ['-updated_on']
    def __str__(self):
        return self.name

BRANCH = (
    (0, "CE"),
    (1, "CS"),
    (2, "EC"),
    (3, "EEE"),
    (4, "IT"),
    (5, "ME"),
    (7, "Branch/Dept")
)

SEM = (
    (0, "S1"),
    (1, "S2"),
    (2, "S3"),
    (3, "S4"),
    (4, "S5"),
    (5, "S6"),
    (6, "S7"),
    (7, "S8"),
    (8, "Semester"),
)

class Participant(models.Model):
    category = models.ForeignKey(Category,on_delete=models.SET_NULL, null=True)
    event = models.ForeignKey(Event, on_delete= models.CASCADE, related_name='events_listed')
    name = models.CharField(max_length=200)
    branch = models.IntegerField(choices=BRANCH, default=7)
    semester = models.IntegerField(choices=SEM, default=8)
    regnumber_regex = RegexValidator(regex=r'^[0-9]{8}$', message="reg number must be entered in the format: '12180222'. Up to 8 digits allowed.")
    regnumber = models.CharField(validators=[regnumber_regex], max_length=8, blank=False, default='')
    phone_regex = RegexValidator(regex=r'^[0-9]{10}$', message="Phone number must be entered in the format: '9876543210'. 10 digits .")
    contact = models.CharField(validators=[phone_regex], max_length=10, blank=False, default='')
    updated_on = models.DateTimeField(default=timezone.now)
    payment = models.BooleanField(default=False)

    class Meta:
        ordering = ['-updated_on']

    def clean(self):
        is_new = True if not self.id else False
        flagind = self.__class__.objects.filter(regnumber=self.regnumber).filter(event__eventtype=0).count()
        flaggrp = self.__class__.objects.filter(regnumber=self.regnumber).filter(event__eventtype=1).count()
        ev = self.event
        type = Event.objects.get(name=ev)
        if is_new:
            if  flagind < 5:
                print("Eligble for Individual Event Registraion")
            elif type.eventtype==0:
                raise forms.ValidationError(" already exists 5 entry : The person already registerd for 5 Ind events, Check the person status here ")
            if flaggrp < 5:
                print("Eligble for Group Event Registraion")
            elif type.eventtype==1:
                raise forms.ValidationError(" already exists 5 entry : The person already registerd for 5 Group events, Check the person status here ")

            if self.__class__.objects.filter(branch=self.branch).filter(event=self.event).count() >= self.event.max_participants:
                raise forms.ValidationError("max 4 Participant only")
        if self.payment == True:
            payupdate = self.__class__.objects.filter(branch=self.branch).filter(event=self.event)
            payupdate.update(payment=True)

    def publish(self):
        self.updated_on = timezone.now()
        self.save()

    def __str__(self):
        return self.name
