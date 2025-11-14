from django.db import models

class Estudiante(models.Model):
    student_id = models.CharField(max_length=10, default="S0000")
    name = models.CharField(max_length=100)
    age = models.IntegerField(default=18)
    gender = models.CharField(max_length=1)
    university = models.CharField(max_length=50)
    faculty = models.CharField(max_length=50)
    year = models.IntegerField(default=1)
    rent_total = models.FloatField(default=0)
    expected_rent = models.FloatField(default=0)
    district = models.CharField(max_length=50)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    has_pets = models.BooleanField(default=False)
    smoker = models.BooleanField(default=False)
    max_commute_min = models.IntegerField(default=30)

    def __str__(self):
        return f"{self.name} ({self.student_id})"
