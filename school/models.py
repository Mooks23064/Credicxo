from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.

# create table for student details
class Student(models.Model):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # Attributes
    email = models.EmailField(_('email_address'), unique=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    student_class = models.IntegerField()
    age = models.IntegerField()
    mentor = models.CharField(max_length=40)
    phone = models.CharField(max_length=10)
    user_role = models.CharField(max_length=16, default="student")


    def __str__(self):
        return "{}".format(self.email)
#create table for teacher details

class Teacher(models.Model):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    # objects = UserManager()

    # Attributes
    email = models.EmailField(_('email_address'), unique=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    allotted_class = models.IntegerField()
    age = models.IntegerField()
    student_name = models.CharField(max_length=40)
    phone = models.CharField(max_length=10)
    user_role = models.CharField(max_length=16, default="teacher")


    def __str__(self):
        return "{}".format(self.email)
#create table for admin

class Admin(models.Model):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    # objects = UserManager()


    # Attributes
    email = models.EmailField(_('email_address'), unique=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phone = models.CharField(max_length=10)
    user_role = models.CharField(max_length=16, default="super_admin")


    def __str__(self):
        return "{}".format(self.email)