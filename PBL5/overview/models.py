from django.db import models

# Create your models here.

class Account(models.Model):
    fullname = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to='avatar/', default= 'avatar/null.png', blank=False)

    def __str__(self):
        return self.fullname