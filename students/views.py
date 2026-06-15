from django.shortcuts import render

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Student,Teacher


def fetch_student_data(request):
    student_list =[]
    students = Student.objects.all()
    for student in students:
        student_list.append({"name":student.name, "score":student.score,"teacher":student.teacher.name})
    return JsonResponse(student_list,safe=False)

# Add to students/views.py and students/urls.py:
#
# 1. GET /student/by_teacher/<int:teacher_id>/
#    → Return all students for that teacher
#
# 2. POST /student/create/
#    → Accept name, score, teacher_id
#    → Create new student in database
#    → Return 201 on success

import json

def get_student_by_teacher(request,teacher_id):
    if request.method == "GET":
        student_data = Student.objects.filter(teacher__id = teacher_id)
        student_list = []
        for student in student_data:
            student_list.append({"name":student.name, "score":student.score,"teacher":student.teacher.name})
        if not student_data:
           return JsonResponse({"message":"Data not Found"},status=404)
        return JsonResponse(student_list,safe=False)
    else:
        return JsonResponse({"message":"Method not allowed"},status=405)

@csrf_exempt
def create_student(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            name = data.get("name")
            score = data.get("score")
            teacher_id = data.get("teacher_id")
            if not name or not score or not teacher_id:
                return JsonResponse({"message":"Missing data"}, status=400)
            try:
                Student.objects.create(name=name, score=int(score), teacher_id = teacher_id)
                return JsonResponse({"message":"Student created successfully"},status=201)
            except ValueError:
                return JsonResponse({"message":"Enter valid data"},status=400)
        except json.decoder.JSONDecodeError:
            return JsonResponse({"message":"Something went wrong"}, status=500)
    else:
        return JsonResponse({"message":"Method not allowed"},status=405)


@csrf_exempt
def update_student(request,student_id):
    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            new_score = data.get("score")
            student = Student.objects.get(id=student_id)
            student.score = new_score
            student.save()
            return JsonResponse({"message":"Student updated successfully"},status=200)
        except Student.DoesNotExist:
            return JsonResponse({"message":"Student not Found"},status=404)
    else:
        return JsonResponse({"message":"Method not allowed"},status=405)

@csrf_exempt
def delete_student(request,student_id):
    if request.method == "DELETE":
        try:
            student = Student.objects.get(id=student_id)
            student.delete()
            return JsonResponse({"message":"Student deleted successfully"},status=200)
        except Student.DoesNotExist:
            return JsonResponse({"message":"Student not found"},status=404)
    else:
        return JsonResponse({"message":"Method not allowed"},status=405)


# Add one more endpoint:
#
# GET /student/stats/
# → Return:
#    - total number of students
#    - highest score
#    - lowest score
#    - average score


def get_stats(request):
    if request.method == "GET":
        student_data = Student.objects.all()
        if not student_data:
            return JsonResponse({"message":"Data not Found"},status=404)
        student_score = []
        for student in student_data:
            student_score.append(student.score)
        resp = {
            "Total_students":len(student_data),
            "Highest Score":max(student_score),
            "Lowest Score":min(student_score),
            "Average Score":sum(student_score)/len(student_score),
        }
        return JsonResponse(resp,safe=False)
    else:
        return JsonResponse({"message":"Method not allowed"},status=405)



# Add one more endpoint:
#
# GET /student/search/?name=Kumaresan
# → Search student by name using query parameter
# → Return student details if found
# → Return 404 if not found

def search_student(request):
    if request.method == "GET":
        try:
            name = request.GET.get("name")
            if not name:
                return JsonResponse({"message":"Name is required"},status=400)
            student_data = Student.objects.filter(name=name)
            if not student_data:
                return JsonResponse({"message":"Data not Found"},status=404)
            student_list = []
            for student in student_data:
                student_list.append({"name":student.name,"score":student.score,"teacher":student.teacher.name})
            return JsonResponse(student_list,safe=False)
        except ValueError:
            return JsonResponse({"message":"Enter valid data"},status=400)
    else:
        return JsonResponse({"message":"Method not allowed"},status=405)