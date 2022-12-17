from django.db import models
from user.models import Student
# Create your models here.

class Log(models.Model):
    date_time = models.DateTimeField()
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.date_time} - {self.student.fullname}"
    