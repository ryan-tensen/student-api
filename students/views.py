from django.shortcuts import render

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Student,Teacher
from .serializers import StudentSerializer, TeacherSerializer


# def fetch_student_data(request):
#     student_list =[]
#     students = Student.objects.all()
#     for student in students:
#         student_list.append({"name":student.name, "score":student.score,"teacher":student.teacher.name})
#     return JsonResponse(student_list,safe=False)


@api_view(["GET"])
def fetch_student_data(request):
    students = Student.objects.all()
    serializer = StudentSerializer(students,many=True)
    return Response(serializer.data)



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

# @csrf_exempt
# def create_student(request):
#     if request.method == "POST":
#         try:
#             data = json.loads(request.body)
#             name = data.get("name")
#             score = data.get("score")
#             teacher_id = data.get("teacher_id")
#             if not name or not score or not teacher_id:
#                 return JsonResponse({"message":"Missing data"}, status=400)
#             try:
#                 Student.objects.create(name=name, score=int(score), teacher_id = teacher_id)
#                 return JsonResponse({"message":"Student created successfully"},status=201)
#             except ValueError:
#                 return JsonResponse({"message":"Enter valid data"},status=400)
#         except json.decoder.JSONDecodeError:
#             return JsonResponse({"message":"Something went wrong"}, status=500)
#     else:
#         return JsonResponse({"message":"Method not allowed"},status=405)

@api_view(["POST"])
def create_student(request):
    serializer = StudentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message":"Student created successfully"}, status=201)
    else:
        return Response(serializer.errors, status=400)


# @csrf_exempt
# def update_student(request,student_id):
#     if request.method == "PUT":
#         try:
#             data = json.loads(request.body)
#             new_score = data.get("score")
#             student = Student.objects.get(id=student_id)
#             student.score = new_score
#             student.save()
#             return JsonResponse({"message":"Student updated successfully"},status=200)
#         except Student.DoesNotExist:
#             return JsonResponse({"message":"Student not Found"},status=404)
#     else:
#         return JsonResponse({"message":"Method not allowed"},status=405)


@api_view(["PUT"])
def update_student(request,student_id):
    try:
        serializer = StudentSerializer(data=request.data,instance=Student.objects.get(id=student_id),partial=True)
    except Student.DoesNotExist:
        return Response({"message":"Student not found"},status=404)
    if serializer.is_valid():
        serializer.save()
        return Response({"message":"Student updated successfully"}, status=200)
    else:
        return Response(serializer.errors, status=400)



# @csrf_exempt
# def delete_student(request,student_id):
#     if request.method == "DELETE":
#         try:
#             student = Student.objects.get(id=student_id)
#             student.delete()
#             return JsonResponse({"message":"Student deleted successfully"},status=200)
#         except Student.DoesNotExist:
#             return JsonResponse({"message":"Student not found"},status=404)
#     else:
#         return JsonResponse({"message":"Method not allowed"},status=405)


@api_view(["DELETE"])
def delete_student(request,student_id):
    try:
        student = Student.objects.get(id=student_id)
        student.delete()
        return Response({"message":"Student deleted successfully"}, status=200)
    except Student.DoesNotExist:
        return Response({"message":"Student not found"},status=404)

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


# Create a TeacherSerializer and add two endpoints:
#
# 1. GET /teacher/all/ → fetch all teachers
# 2. POST /teacher/create/ → create new teacher
#    → Accept name, email
#    → Validate with serializer

@api_view(["GET"])
def all_teachers(request):
    try:
        teacher = Teacher.objects.all()
        teacher_data = TeacherSerializer(teacher,many=True)
        return Response(teacher_data.data)
    except Teacher.DoesNotExist:
        return JsonResponse({"message":"Teacher not found"},status=404)


@api_view(["POST"])
def create_teacher(request):
    serializer = TeacherSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message":"Teacher created successfully"}, status=201)
    else:
        return Response(serializer.errors, status=400)


from rest_framework import viewsets,filters
from django_filters.rest_framework import DjangoFilterBackend

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = (DjangoFilterBackend,filters.OrderingFilter,filters.SearchFilter)
    filterset_fields = ['name','score','teacher']
    search_fields = ['name']
    ordering_fields = ['score','name']

    def partial_update(self,request,*args,**kwargs):
        kwargs["partial"] = True
        return self.update(request,*args,**kwargs)


# Create a TeacherViewSet:
# 1. Add ViewSet for Teacher model
# 2. Register with router
# 3. Test all 5 endpoints in Postman:
#    - GET all teachers
#    - GET single teacher
#    - POST create teacher
#    - PATCH update teacher
#    - DELETE teacher


# Add filtering to TeacherViewSet:(18-06-2026)
# 1. Filter by name
# 2. Search by name
# 3. Order by name

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = (DjangoFilterBackend,filters.OrderingFilter,filters.SearchFilter)
    filterset_fields = ['name','email','id']
    ordering_fields = ['name','id']
    search_fields = ['name']

    def partial_update(self,request,*args,**kwargs):
        kwargs["partial"] = True
        return self.update(request,*args,**kwargs)

