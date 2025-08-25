
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from .forms import LabRegistrationForm, IsolateForm, TestResultForm
from .models import Lab, Isolate, TestResult, Antibiotic

def home(request):
    total_labs = Lab.objects.count()
    total_tests = TestResult.objects.count()
    context = {
        'total_labs': total_labs,
        'total_tests': total_tests,
    }
    return render(request, 'home.html', context)

def register(request):
    if request.method == 'POST':
        form = LabRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('lab_dashboard')
    else:
        form = LabRegistrationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def lab_dashboard(request):
    try:
        lab = request.user.lab
        isolates = lab.isolates.all().order_by('-created_at')[:10]
        context = {
            'lab': lab,
            'isolates': isolates,
        }
        return render(request, 'lab_dashboard.html', context)
    except Lab.DoesNotExist:
        messages.error(request, 'No lab associated with this user.')
        return redirect('home')

@login_required
def submit_isolate(request):
    if request.method == 'POST':
        form = IsolateForm(request.POST)
        if form.is_valid():
            isolate = form.save(commit=False)
            isolate.lab = request.user.lab
            isolate.save()
            messages.success(request, 'Isolate submitted successfully!')
            return redirect('submit_results', isolate_id=isolate.id)
    else:
        form = IsolateForm()
    return render(request, 'submit_isolate.html', {'form': form})

@login_required
def submit_results(request, isolate_id):
    isolate = get_object_or_404(Isolate, id=isolate_id, lab=request.user.lab)
    
    if request.method == 'POST':
        form = TestResultForm(request.POST)
        if form.is_valid():
            for field_name, result in form.cleaned_data.items():
                if result and field_name.startswith('antibiotic_'):
                    antibiotic_id = int(field_name.split('_')[1])
                    antibiotic = Antibiotic.objects.get(id=antibiotic_id)
                    TestResult.objects.update_or_create(
                        isolate=isolate,
                        antibiotic=antibiotic,
                        defaults={'result': result}
                    )
            messages.success(request, 'Test results submitted successfully!')
            return redirect('lab_dashboard')
    else:
        form = TestResultForm()
    
    return render(request, 'submit_results.html', {'form': form, 'isolate': isolate})

def dashboard(request):
    # Public dashboard
    total_labs = Lab.objects.count()
    total_isolates = Isolate.objects.count()
    total_tests = TestResult.objects.count()
    
    # Simple statistics
    resistance_stats = TestResult.objects.values('result').annotate(count=Count('result'))
    
    context = {
        'total_labs': total_labs,
        'total_isolates': total_isolates,
        'total_tests': total_tests,
        'resistance_stats': resistance_stats,
    }
    return render(request, 'dashboard.html', context)

def about(request):
    return render(request, 'about.html')