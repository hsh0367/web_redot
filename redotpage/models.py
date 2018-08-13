from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.utils import timezone


class Board(models.Model):
    number = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=200)
    board_title = models.CharField(max_length=200,blank=False)
    message = models.TextField()
    create_date = models.DateField('Create Date', auto_now_add=True)
    hit=models.IntegerField(default=0)
    modify_date = models.DateField('Modify Date', auto_now=True)

    def publish(self):
        self.create_date = timezone.now()
        self.save()

    def __str__(self):
        return self.user_id

class SignupUser(models.Model):
    created_time = models.DateTimeField(auto_now=True)
    updated_time = models.DateTimeField(auto_now=True)
    email = models.EmailField(max_length=128,unique=True)
    username = models.CharField(max_length=50,unique=True)
    password1 = models.CharField(max_length=255)
    password2 = models.CharField(max_length=255)
    active = models.BooleanField(default=False)

    def publish(self):
        self.create_date = timezone.now()
        self.save()

    def __str__(self):
        return self.username


class TestUser(User):
    active = models.BooleanField(default=False)

    def publish(self):
        self.create_date = timezone.now()
        self.save()

    def __str__(self):
        return self.username
