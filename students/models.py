from django.db import models

class Teacher(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField(max_length=254)

class Student(models.Model):
    name = models.CharField(max_length=120)
    score = models.IntegerField(default=0)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
