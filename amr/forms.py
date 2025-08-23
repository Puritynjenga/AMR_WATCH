from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Lab, Isolate, TestResult, Antibiotic

class LabRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    lab_name = forms.CharField(max_length=200, required=True)
    location = forms.CharField(max_length=200, required=True)
    lab_type = forms.ChoiceField(choices=Lab.LAB_TYPE_CHOICES, required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'lab_name', 'location', 'lab_type']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            Lab.objects.create(
                user=user,
                name=self.cleaned_data['lab_name'],
                location=self.cleaned_data['location'],
                lab_type=self.cleaned_data['lab_type']
            )
        return user

class IsolateForm(forms.ModelForm):
    class Meta:
        model = Isolate
        fields = ['bacteria_name', 'sample_type', 'test_date']
        widgets = {
            'test_date': forms.DateInput(attrs={'type': 'date'}),
        }

class TestResultForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for antibiotic in Antibiotic.objects.all():
            self.fields[f'antibiotic_{antibiotic.id}'] = forms.ChoiceField(
                choices=[('', '---')] + TestResult.RESULT_CHOICES,
                required=False,
                label=antibiotic.name
            )