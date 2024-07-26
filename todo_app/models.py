from django.db import models
from django.contrib.auth.models import User

# Create your models here.
'''
def Massage(models.Model):
    name = models.CharField(max_length=33)
    date = models.DateTimeField()
    login = models.CharField(max_length=33)
    tittle = models.CharField(max_length=500)
    massage = models.Text()

'''

class Todo(models.Model):
    title = models.CharField(max_length=100)
    memo = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

