from django.urls import path

from .views import fetch_student_data

urlpatterns = [
            path("fetch_student_data/",fetch_student_data),
]