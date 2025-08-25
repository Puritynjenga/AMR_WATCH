

# Register your models here.
from django.contrib import admin
from .models import Lab, Antibiotic, Isolate, TestResult

@admin.register(Lab)
class LabAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'lab_type', 'created_at']
    search_fields = ['name', 'lab_type']

@admin.register(Antibiotic)
class AntibioticAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    search_fields = ['name']

@admin.register(Isolate)
class IsolateAdmin(admin.ModelAdmin):
    list_display = ['bacteria_name', 'lab', 'sample_type', 'test_date']
    list_filter = ['sample_type', 'test_date']
    search_fields = ['bacteria_name']

@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ['isolate', 'antibiotic', 'result', 'created_at']
    list_filter = ['result', 'created_at']
