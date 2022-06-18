from django.db import models
 
# Create your models here.

  
# class Course (models.Model):
#     course_id = models.CharField(max_length=4)
#     course_name = models.CharField(max_length=20)
#     course_details = models.CharField(max_length=100)
class Profile(models.Model):
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

class Question (models.Model):
    
    question_token = models.CharField(max_length=50, default=None)
    question_username = models.CharField(max_length=50, default=None)
    question_name = models.CharField(verbose_name="Question",max_length=50, default=None)
    question_language = models.CharField(verbose_name="Language",max_length=10)
    question_source = models.TextField()
    question_condition = models.CharField(max_length=100, default=None)
    question_element = models.CharField(max_length=50, default=None)
    
    

        