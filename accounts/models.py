from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import os
from django.utils import timezone

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    basefilename, file_extension= os.path.splitext(filename)
    timenow = timezone.now()
    return 'profile/{userid}/{basename}{time}{ext}'.format(userid=instance.user.id, basename=basefilename, time=timenow.strftime("%Y%m%d%H%M%S"), ext=file_extension)
ROLE = (
    (0, "Participant"),
    (1, "Volunteer"),
    (2, "Branch Captian"),
    (3, "Admin"),
    (4,"Visitor"),
)

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




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.IntegerField(choices=ROLE, default=4)
    branch = models.IntegerField(choices=BRANCH, default=7)
    semester = models.IntegerField(choices=SEM, default=8)
    profile = models.ImageField(upload_to=user_directory_path, default='profile.png',help_text="Profile Picture")
    contact = models.IntegerField(max_length=10, blank=True, default="Mobile Number")
    location = models.CharField(max_length=30, blank=True, default="CUCEK", help_text="eg:- College Name, organization name ..etc")
    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
