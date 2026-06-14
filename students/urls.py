from django.urls import path

from .views import fetch_student_data, get_student_by_teacher, create_student

urlpatterns = [
            path("fetch_student_data/",fetch_student_data),
            path("get_student_by_teacher/<int:teacher_id>/",get_student_by_teacher),
            path("create_student/",create_student)
]