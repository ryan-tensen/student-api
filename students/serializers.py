from rest_framework import serializers
from .models import Student,Teacher

class StudentSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source="teacher.name",read_only=True)
    class Meta:
        model = Student
        fields = ["id","name","score","teacher","teacher_name"]

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ["id","name","email"]