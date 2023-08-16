from rest_framework import serializers
from .models import TestTitle, Report, Test

class TestTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestTitle
        fields = '__all__'

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = '__all__'

class ReportSerializer(serializers.ModelSerializer):
    tests = TestSerializer(many=True, read_only=True)

    class Meta:
        model = Report
        fields = '__all__'
