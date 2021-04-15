from rest_framework import serializers
from school.models import Student, Teacher
from account.models import User
from django.utils.translation import ugettext_lazy as _

# for student details
class StudentViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

# for teacher detail
class TeacherViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'

# teacher have permission to create student
class TeacherStudentViewSerializer(serializers.ModelSerializer):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # Attributes
    email = serializers.EmailField(max_length=30)
    first_name = serializers.CharField(max_length=20)
    last_name = serializers.CharField(max_length=20)
    student_class = serializers.IntegerField()
    age = serializers.IntegerField()
    mentor = serializers.CharField(max_length=40)
    phone = serializers.CharField(max_length=10)
    user_role = serializers.CharField(max_length=10, default="student")

    class Meta:
        model = Student
        fields = '__all__'

# for profile details
class DetailViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'user_role',
        )