
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from account.models import User
from school.models import Student, Teacher
from school.serializers import StudentViewSerializer, TeacherViewSerializer, DetailViewSerializer
# from school.serializers import DetailViewSerializer
# Create your views here.

class UserProfileView(generics.GenericAPIView):

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication   # token validation
    serializer_class = DetailViewSerializer
    def get(self, request):
        try:
            user_profile = User.objects.get(email=request.user)     # fetch valid user

            status_code = status.HTTP_200_OK
            response = {
                'success': 'true',
                'status code': status_code,
                'message': 'User profile fetched successfully',
                'data': self.serializer_class(user_profile).data,

                }

        except Exception as e:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': 'false',
                'status code': status.HTTP_400_BAD_REQUEST,
                'message': 'User does not exists',
                }
        return Response(response,status=status_code)

class StudentProfileView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication   # token validation
    serializer_class = StudentViewSerializer

    def get(self, request):
        try:
            user_profile = Student.objects.get(email=request.user)      # fetch data by email from student table only valid user
            if user_profile.user_role == "student":
                status_code = status.HTTP_200_OK
                response = {
                    'success': 'true',
                    'status code': status_code,
                    'message': 'User profile fetched successfully',
                    'data': self.serializer_class(user_profile).data,

                }
            else:
                status_code = status.HTTP_203_NON_AUTHORITATIVE_INFORMATION
                response = {
                    'success': 'false',
                    'status code': status_code,
                    'message': 'Have not permission',
                }

        except Exception as e:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': 'false',
                'status code': status.HTTP_400_BAD_REQUEST,
                'message': 'User does not exists',
            }
        return Response(response, status=status_code)

class TeacherView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    serializer_class = TeacherViewSerializer

    def get(self, request):
        try:
            user_profile = Teacher.objects.get(email=request.user)  #fetch all data of valid teacher from teacher table
            if user_profile.user_role == "teacher":
                status_code = status.HTTP_200_OK
                response = {
                    'success': 'true',
                    'status code': status_code,
                    'message': 'User profile fetched successfully',
                    'data': self.serializer_class(user_profile).data,

                }

            else:
                status_code = status.HTTP_203_NON_AUTHORITATIVE_INFORMATION
                response = {
                    'success': 'false',
                    'status code': status_code,
                    'message': 'Not have permission',
                }
        except Exception as e:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': 'false',
                'status code': status.HTTP_400_BAD_REQUEST,
                'message': 'User does not exists',
            }
        return Response(response, status=status_code)

# to create and view student

class TeacherStudentView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication       #for token validation
    serializer_class = StudentViewSerializer

# to view all student in school
    def get(self, request):
        user_profile = User.objects.get(email=request.user)
        if user_profile.user_role == "teacher":
            student = Student.objects.all()
            serializer = StudentViewSerializer(student, many=True)
            return Response(serializer.data)

# to add student by their email address only by teacher
    def post(self, request):
        try:
            user_profile = User.objects.get(email=request.user)
            if user_profile.user_role == "teacher":
                serializer = self.serializer_class(data=request.data)
                if serializer.is_valid():
                    new_user = serializer.save()
                    if new_user:
                        status_code= status.HTTP_201_CREATED
                        response={
                                "data": new_user,
                                "message": "successfull created",
                                "status": status.HTTP_201_CREATED,
                            }
                else:
                    status_code=status.HTTP_400_BAD_REQUEST
                    response= {
                            "message": serializer.errors,
                            "status": status.HTTP_400_BAD_REQUEST
                        }

        except Exception as e:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': 'false',
                'status code': status.HTTP_400_BAD_REQUEST,
                'message': 'User does not exists',
            }

            return Response(response, status=status_code)




