from django.db import models
from django.utils import timezone


class Board(models.Model):
    number = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=200)
    board_title = models.CharField(max_length=200,blank=False)
    message = models.TextField()
    create_date = models.DateField('Create Date', auto_now_add=True)
    hit = models.IntegerField(default=0)
    modify_date = models.DateField('Modify Date', auto_now=True)

    def publish(self):
        self.create_date = timezone.now()
        self.save()

    def __str__(self):
        return self.user_id

'''
class RedotUser(User):
    is_active = models.BooleanField(default=False)
    create_date = models.DateField(auto_now_add=True, blank=True)

    def publish(self):
        self.create_date = timezone.now()
        self.save()

    def __str__(self):
        return self.username
'''

