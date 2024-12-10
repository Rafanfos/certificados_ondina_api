import uuid
from django.db import models


class Student(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=255)
    graduation_term = models.CharField(max_length=50)
    diploma_generated = models.BooleanField(default=False)
    highlight_certificate_generated = models.BooleanField(default=False)


class Highlight_Certificate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="highlight_certificates"
    )
    generated_at = models.DateTimeField(auto_now_add=True)
    director_name = models.CharField(
        max_length=255,
    )
    vice_director_name = models.CharField(max_length=255)

    def __str__(self):
        return f"Certificate for {self.student.full_name} - {self.generated_at}"


class Diploma(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="diploma"
    )
    generated_at = models.DateTimeField(auto_now_add=True)
    director_name = models.CharField(
        max_length=255,
    )

    def __str__(self):
        return f"Diploma for {self.student.full_name} - {self.generated_at}"
