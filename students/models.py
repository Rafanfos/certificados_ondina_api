from django.db import models

# Create your models here.

class Student(models.Model):
    full_name = models.CharField(max_length=255)
    graduation_term = models.IntegerField()
    diploma_generated = models.BooleanField(default=False) 
    best_student_certificate_generated = models.BooleanField(default=False)  

    def __str__(self):
        return self.full_name
    
class HighlightCertificate(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    generated_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Certificate for {self.student.full_name} generated on {self.generated_date.strftime('%Y-%m-%d')}"