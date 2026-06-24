from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, EnrollmentViewSet

urlpatterns = [
        # path("create_course",)
]

default_router = DefaultRouter()
default_router.register('enrollment', EnrollmentViewSet)
default_router.register('course', CourseViewSet)
urlpatterns += default_router.urls