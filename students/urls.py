from django.urls import path

from .views import fetch_student_data, get_student_by_teacher, create_student, update_student, delete_student, \
    get_stats, search_student, all_teachers, create_teacher

urlpatterns = [
            path("fetch_student_data/",fetch_student_data),
            path("get_student_by_teacher/<int:teacher_id>/",get_student_by_teacher),
            path("create_student/",create_student),
            path("update_student/<int:student_id>/",update_student),
            path("delete_student/<int:student_id>/",delete_student),
            path("get_stats/",get_stats),
            path("search_student/",search_student),
            path("all_teachers/",all_teachers),
            path("create_teacher/",create_teacher)
]