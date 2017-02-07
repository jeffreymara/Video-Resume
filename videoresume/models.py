from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class User_Info(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=64,blank=True)
    first_name = models.CharField(max_length=64,blank=True)
    last_name = models.CharField(max_length=64,blank=True)
    email = models.CharField(max_length=128,blank=True)
    location = models.CharField(max_length=128,blank=True)
    date_created = models.DateTimeField(default=datetime.now, blank=True)
    screen_width = models.IntegerField(blank=True)
    phone_number = models.CharField(max_length=32,blank=True)
    verification = models.CharField(max_length=64,blank=True,null=True)
    linkedin_url = models.CharField(max_length=256,blank=True)
    personal_website_url = models.CharField(max_length=256,blank=True)
    profile_image_url = models.CharField(max_length=256,blank=True,null=True)
    summary = models.TextField(blank=True)
    submitted = models.BooleanField(default=False)
    welcome_message = models.BooleanField(default=True)
    help_requested = models.BooleanField(default=False)

    def full_name(self):
        return self.first_name+" "+self.last_name

    def __str__(self):              # __unicode__ on Python 2
        return self.first_name+" "+self.last_name

class File(models.Model):
    user_id = models.ForeignKey(User_Info, on_delete=models.CASCADE)
    name = models.CharField(max_length=128,blank=True)
    upload = models.FileField(upload_to='uploads/',blank=True)
    external_src = models.CharField(max_length=256,blank=True)
    date_created = models.DateTimeField(default=datetime.now, blank=True)
    type = models.CharField(max_length=64,blank=True)
    file_type = models.CharField(max_length=32,blank=True)
    size = models.IntegerField(blank=True)
    uploaded = models.BooleanField(default=False)

    def __str__(self):              # __unicode__ on Python 2
        return self.name

class Blocked_Company(models.Model):
    user_id = models.ForeignKey(User_Info, on_delete=models.CASCADE)
    name = models.CharField(max_length=128,blank=True)
    date_created = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):              # __unicode__ on Python 2
        return self.name

class Job_Location(models.Model):
    user_id = models.ForeignKey(User_Info, on_delete=models.CASCADE)
    name = models.CharField(max_length=128,blank=True)
    date_created = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):              # __unicode__ on Python 2
        return self.name

class Role(models.Model):
    user_id = models.ForeignKey(User_Info, on_delete=models.CASCADE)
    name = models.CharField(max_length=128,blank=True)
    date_created = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):              # __unicode__ on Python 2
        return self.name

class Sub_Role(models.Model):
    role_id = models.ForeignKey(Role, on_delete=models.CASCADE)
    name = models.CharField(max_length=128,blank=True)
    date_created = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):              # __unicode__ on Python 2
        return self.name

class Company(models.Model):
    name = models.CharField(max_length=128,blank=True)
    video_description = models.CharField(max_length=256,blank=True)
    short_description = models.CharField(max_length=256,blank=True)
    date_created = models.DateTimeField(default=datetime.now, blank=True)
    location = models.CharField(max_length=128,blank=True)
    open_roles = models.IntegerField(blank=True)
    profile_image_external = models.CharField(max_length=256,blank=True)
    job_board_external = models.CharField(max_length=256,blank=True)

    def __str__(self):              # __unicode__ on Python 2
        return self.name


