from django.db import models
from django.contrib.auth.models import User

class Lab(models.Model):
    LAB_TYPE_CHOICES = [
        ('hospital', 'Hospital'),
        ('research', 'Research'),
        ('private', 'Private'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    lab_type = models.CharField(max_length=50, choices=LAB_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Antibiotic(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return self.name

class Isolate(models.Model):
    SAMPLE_TYPE_CHOICES = [
        ('blood', 'Blood'),
        ('urine', 'Urine'),
        ('stool', 'Stool'),
        ('sputum', 'Sputum'),
        ('wound', 'Wound'),
        ('other', 'Other'),
    ]
    
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE, related_name='isolates')
    bacteria_name = models.CharField(max_length=200)
    sample_type = models.CharField(max_length=100, choices=SAMPLE_TYPE_CHOICES)
    test_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.bacteria_name} - {self.test_date}"

class TestResult(models.Model):
    RESULT_CHOICES = [
        ('R', 'Resistant'),
        ('I', 'Intermediate'),
        ('S', 'Sensitive'),
    ]
    
    isolate = models.ForeignKey(Isolate, on_delete=models.CASCADE, related_name='results')
    antibiotic = models.ForeignKey(Antibiotic, on_delete=models.CASCADE)
    result = models.CharField(max_length=1, choices=RESULT_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['isolate', 'antibiotic']
    
    def __str__(self):
        return f"{self.isolate.bacteria_name} - {self.antibiotic.name}: {self.result}"