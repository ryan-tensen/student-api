from django.shortcuts import render

from django.http import JsonResponse

from .models import Student


def fetch_student_data(request):
    student_list =[]
    students = Student.objects.all()
    for student in students:
        student_list.append({"name":student.name, "score":student.score,"teacher":student.teacher.name})
    return JsonResponse(student_list,safe=False)
