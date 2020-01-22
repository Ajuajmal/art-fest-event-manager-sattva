from __future__ import unicode_literals
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
    (3, "Finished"),
    (4, "Stage 1"),
    (5, "Stage 2"),
    (6, "Stage 3"),
    (7, "Stage 4"),
    (8, "Stage 5"),
    (9, "Stage 6"),
)

EVENTTYPE = (
    (0,"Individual"),
    (1,"Group"),
)

STAGETYPE = (
    (0,"Onstage"),
    (1,"OffStage"),
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
    eventid =models.CharField(max_length=20, default="EW")
    name = models.CharField(max_length=200)
    stagetype = models.IntegerField(choices=STAGETYPE, default=0)
    eventtype = models.IntegerField(choices=EVENTTYPE, default=0)
    date = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField(default=timezone.now)
    venue = models.IntegerField(choices=VENUE, default=1)
    cover = models.ImageField(upload_to=user_directory_path, default='defaultevent.jpg')
    max_participants = models.IntegerField(default=0)
    accompanying_participants = models.BooleanField(default=False)
    max_accompanying_participants = models.IntegerField(default=0)
    slot =  models.IntegerField(default=1)
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
    (6, "MCA"),
    (7, "Branch/Dept")
)

SEM = (
    (1, "S2"),
    (3, "S4"),
    (5, "S6"),
    (7, "S8"),
    (8, "Semester"),
)


SLOT = (
    (1, "SLOT 1"),
    (2, "SLOT 2"),
    (3, "SLOT 3"),
    (4, "SLOT 4"),
    (5, "SLOT 5"),
    )

PARTICIPANT_TYPE =(
    (0, "Main Participant"),
    (1, "Accompanying Participant"),
    )
class Participant(models.Model):
    category = models.ForeignKey(Category,on_delete=models.SET_NULL, null=True)
    event = models.ForeignKey(Event, on_delete= models.CASCADE, related_name='events_listed')
    slot = models.IntegerField(choices=SLOT, default=1)
    participant_type = models.IntegerField(choices=PARTICIPANT_TYPE, default=0)
    name = models.CharField(max_length=200)
    branch = models.IntegerField(choices=BRANCH, default=7)
    semester = models.IntegerField(choices=SEM)
    regnumber_regex = RegexValidator(regex=r'^[0-9]{8}$', message="reg number must be entered in the format: '12180222'.Only 8 digits reg numbers are allowed. For MCA S6 :- Please remove first digit (1) and enter remaining ")
    regnumber = models.CharField(validators=[regnumber_regex], max_length=8, blank=False, default='')
    updated_on = models.DateTimeField(default=timezone.now)
    deletable = models.BooleanField(default=True)
    substitution = models.BooleanField(default=False)
    spot = models.BooleanField(default=False)
    payment = models.BooleanField(default=False)

    class Meta:
        ordering = ['-updated_on']


    def clean(self):
        is_new = True if not self.id else False
        flagind = self.__class__.objects.filter(regnumber=self.regnumber).filter(event__stagetype=0).filter(event__eventtype=0).filter(participant_type=0).count()
        flaggrp = self.__class__.objects.filter(regnumber=self.regnumber).filter(event__stagetype=0).filter(event__eventtype=1).filter(participant_type=0).count()
        if self.event_id == None:
            raise forms.ValidationError(" error value undefined ")
        ev = self.event_id
        type = Event.objects.get(id=ev)
        if is_new:
            if  flagind < 5:
                print("Eligble for Individual Event Registraion")
            elif type.eventtype==0 and type.stagetype==0:
                raise forms.ValidationError(" already exists 5 entry : The person already registerd for 5 Individual(OnStage) events, Check the participant status.")
            if flaggrp < 5:
                print("Eligble for Group Event Registraion")
            elif type.eventtype==1 and type.stagetype==0:
                raise forms.ValidationError(" already exists 5 entry : The person already registerd for 5 Group(OnStage) events, Check the participant status.")
            if self.slot <= self.event.slot:
                print("Correct Number of Slots Chosen")
            else:
                raise forms.ValidationError("Hey , maximum number of slots available for the {} event is {}. Please select the solt {} or less ".format(self.event,self.event.slot, self.event.slot))
            if self.participant_type == 1 and self.event.accompanying_participants == True:
                print("Accompanying is available for this event")
            elif self.participant_type == 0:
                print("Eligible To Participant Registraion")
            else:
                raise forms.ValidationError("Hey , The {} event does not have accompanying participants option kindly check the event terms one more time.".format(self.event))
            #duplicate Error
            if self.__class__.objects.filter(branch=self.branch).filter(event=self.event).filter(regnumber=self.regnumber).count() <1:
                print("New Duplicate Entry Not Found")
            else:
                raise forms.ValidationError("Duplicate Entry : Hey , Participant, {} was already registered for the event {}".format(self.name,self.event))
            if self.__class__.objects.filter(branch=self.branch).filter(event=self.event).filter(slot=self.slot).filter(participant_type=0).count() >= self.event.max_participants and self.participant_type == 0:
                raise forms.ValidationError("Hey, Your branch has already registerd maximum number of participant(s)({}) for the {} event with slot number {}. Slot Number {} is filled, try other slot numbers. \n For {} , you can try the slot number upto {}".format(self.event.max_participants,self.event,self.slot,self.slot,self.event,self.event.slot))
            if self.__class__.objects.filter(branch=self.branch).filter(event=self.event).filter(slot=self.slot).filter(participant_type=1).count() >= self.event.max_accompanying_participants and self.participant_type == 1:
                raise forms.ValidationError("Hey, Your branch has already registerd maximum number of accompanying participant(s)({}) for the {} event with slot number {}. Slot Number {} is filled, try other slot numbers. \n For {} , you can try the slot number upto {}".format(self.event.max_accompanying_participants,self.event,self.slot,self.slot,self.event,self.event.slot))

        if self.payment == True and self.event.eventtype == 1:
            payupdate = self.__class__.objects.filter(branch=self.branch).filter(event=self.event).filter(slot=self.slot)
            payupdate.update(payment=True)

    def publish(self):
        self.updated_on = timezone.now()
        self.save()

    def __str__(self):
        return '%s %s %s %s %s' % (self.event, self.name, self.get_branch_display(), self.get_semester_display(), self.regnumber)
