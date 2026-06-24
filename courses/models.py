from django.db import models
from django.utils.timezone import now

from students.models import Teacher, Student


class Course(models.Model):
    title = models.CharField(max_length=256)
    duration = models.IntegerField()
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_date  = models.DateField(auto_now_add=True)

