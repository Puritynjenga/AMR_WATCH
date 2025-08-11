from rest_framework import serializers
from .models import models
from .models import User, lab, isolate, amr_result, antibiotic  

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class LabSerializer(serializers.ModelSerializer):
    class Meta:
        model = lab
        fields = '__all__'

class IsolateSerializer(serializers.ModelSerializer):
    class Meta:
        model = isolate
        fields = '__all__'

class AMRResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = amr_result
        fields = '__all__'

class AntibioticSerializer(serializers.ModelSerializer):
    class Meta:
        model = antibiotic
        fields = '__all__'
