from django.db import models
import datetime
from django.conf import settings
# Create your models here.

class Category(models.Model):
    name=models.CharField(default="test",max_length=50,null=False,primary_key=True)



class Task(models.Model):

    SET_OF_CHOICES = (
        ('choice1', 'Low'),
        ('choice2', 'Medium'),
        ('choice3', 'Hard'),
        
    )
    name=models.CharField(max_length=255,null=False)
    due_date=models.DateTimeField(null=False)
    creation_date=models.DateTimeField(auto_now_add=True)
    last_updated=models.DateTimeField(auto_now=True)
    status=models.BooleanField(default=False)
    postpones=models.IntegerField(default=0)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    description=models.TextField()
    priority=models.CharField(choices=SET_OF_CHOICES,max_length=10)
    restored=models.BooleanField(default=False)
    first_created=models.DateField(default=datetime.date(1998, 12, 25))
    old_id = models.IntegerField(default=0,null=True)
    



class RecycleBin(models.Model):

    name=models.CharField(max_length=255,null=False)
    due_date=models.DateTimeField(null=False)
    creation_date=models.DateTimeField()
    last_updated=models.DateTimeField()
    status=models.BooleanField(default=False)
    postpones=models.IntegerField(default=0)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    description=models.TextField()
    priority=models.CharField(max_length=10)
    idd=models.IntegerField(default=0)
    