from django.urls import path
from school import views

urlpatterns = [
    path('profile/', views.UserProfileView.as_view()),
    path('student/', views.StudentProfileView.as_view()),
    path('teacher/student/', views.TeacherStudentView.as_view()),
    path('teacher/', views.TeacherView.as_view()),

]
