import email
from django.db import models

# Create your models here.

class Student(models.Model):
    code = models.CharField(max_length=10)
    fullname = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to='avatar/', default= 'avatar/null.png', blank=False)

    def __str__(self):
        return f"{self.code} - {self.name}({self.id})"
