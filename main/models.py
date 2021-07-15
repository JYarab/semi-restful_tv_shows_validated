from django.db import models
from datetime import datetime


# Create your models here.

class ShowManager(models.Manager):
    def basic_validator(self, postData):

        shows = Show.objects.all()
        errors = {}

        if len(postData['title']) < 2:
            errors['title'] = 'Title must be at least 2 charaters'
        else:
            for show in shows:
                if postData['title'] == show.title:
                    errors['title'] = 'Title must be unique'
        
        if len(postData['network']) < 3:
            errors['network'] = 'Network must be at least 3 charaters'

        if len(postData['date']) == 0:
            errors['date'] = 'Must include release date'
        
        if len(postData['desc']) > 0 and len(postData['desc']) < 10:
            errors['desc'] = 'Description must be at least 10 charaters'
        
        if datetime.strptime(postData['date'], '%Y-%m-%d') > datetime.now(): 
            errors['date'] = 'Release date must be in the past'

        return errors

class Show(models.Model):
    title = models.CharField(max_length=255)
    network = models.CharField(max_length=255)
    release_date = models.DateField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ShowManager()


