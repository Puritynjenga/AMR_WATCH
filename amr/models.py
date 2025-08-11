from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.username
    
class lab(models.Model):
    name = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name  

class isolate(models.Model):
    name = models.CharField(max_length=100)
    lab = models.ForeignKey(lab, on_delete=models.CASCADE, related_name='isolates')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    date_collected = models.DateField()
    type = models.CharField(max_length=100)
    specimen_type = models.CharField(max_length=100)

    def __str__(self):
        return self.name      
    
class amr_result(models.Model):
    isolate = models.ForeignKey(isolate, on_delete=models.CASCADE, related_name='amr_results')
    antibiotic = models.CharField(max_length=100)
    result = models.CharField(max_length=50)  # e.g., 'resistant', 'susceptible'
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.isolate.name} - {self.antibiotic} - {self.result}"
    
class antibiotic(models.Model):
    name = models.CharField(max_length=100, unique=True)
    mechanism_of_action = models.TextField()
    spectrum_of_activity = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name    