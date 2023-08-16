from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .models import Report,TestTitle,Test
from account.models import Patient
from doctor.models import Doctor
from booking.models import Booking
from .serializers import ReportSerializer,TestSerializer,TestTitleSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import CreateAPIView
# Create your views here.

@api_view(['GET'])
def getRoutes(request):
    routes = [
        'report/list',
       
    ]
    return Response(routes)

class ReportCreateView(APIView):
    def post(self, request, format=None):
        serializer = ReportSerializer(data=request.data)

        if serializer.is_valid():
            # If the serializer is valid, save the report and return a success response
            serializer.save()
            # print(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # If the serializer is not valid, return an error response with validation errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class ReportRetriveView(APIView):
    def get(self,request,booking_id,format=None):
       
        report = get_object_or_404(
            Report,
            booking_id=booking_id,
            
        )

        serializer=ReportSerializer(report)

        return Response(serializer.data)
    
class ReportUpdateView(APIView):
    def put(self, request, *args, **kwargs):
        report_id = kwargs['report_id']
        report = Report.objects.get(pk=report_id)
        serializer= ReportSerializer(report,data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_test_titles(request):
   
    tes_titles=TestTitle.objects.all()
    serializer=TestTitleSerializer(tes_titles,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)

# class TestCreateView(CreateAPIView):
    
#     serializer_class = TestSerializer
#     queryset = Test.objects.all()

class TestReportCreateView(APIView):
    def post(self, request, format=None):
        print(request.data)
        serializer = TestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
