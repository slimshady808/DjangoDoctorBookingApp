from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .models import *
from .serializers import *
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import CreateAPIView
from django.shortcuts import get_object_or_404
from account.models import UserProfile
from doctor.models import Doctor
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import RetrieveUpdateAPIView,ListCreateAPIView,RetrieveUpdateDestroyAPIView
# Create your views here.


@api_view(['GET'])
def getRoutes(request):
    routes = [
        'report/list',
       
    ]
    return Response(routes)

class NoPagination(PageNumberPagination):
    page_size = None


class ReportCreateView(APIView):
    def post(self, request, format=None):
        doc=request.data["doctor_id"]
    
        user=UserProfile.objects.get(id=doc)
        doctor=Doctor.objects.get(user_profile=user)
        # print('last',doctor.id)
        request.data["doctor_id"]=doctor.id
        serializer = ReportSerializer(data=request.data)
        print('before',request.data)
        if serializer.is_valid():
            # print('after',serializer.data)
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
        print(request.data)
        doc=request.data["doctor_id"]
        user=UserProfile.objects.get(id=doc)
        doctor=Doctor.objects.get(user_profile=user)
        request.data["doctor_id"]=doctor.id
        report_id = kwargs['report_id']
        report = Report.objects.get(pk=report_id)

        serializer= ReportSerializer(report,data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET'])
# def get_test_titles(request):
   
#     tes_titles=TestTitle.objects.all()
#     serializer=TestTitleSerializer(tes_titles,many=True)
#     return Response(serializer.data,status=status.HTTP_200_OK)


class TestReportCreateView(APIView):
    def post(self, request, format=None):
        print(request.data)
        serializer = TestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class GetTestsByReportView(APIView):
    def get(self, request, report_id):
        try:
            report = Report.objects.get(pk=report_id)
            tests = Test.objects.filter(report=report)
            response_data=[]
            for test in tests:
                response_data.append({
                    'test_id':test.id,
                    'test_name':test.test_title.test_name,
                    'test_date':test.date_of_test,
                    'notes':test.notes,
                    'result':test.result.url  # Get the URL of the uploaded file
                })
            return Response(response_data, status=status.HTTP_200_OK)

        except Report.DoesNotExist:
            return Response({"error": "Report does not exist."}, status=status.HTTP_404_NOT_FOUND)

class DeleteTestView(APIView):
    def delete(request,self,test_id):
        test=get_object_or_404(Test,pk=test_id)
        test.delete()
        return Response({'data':'deleted'},status=status.HTTP_204_NO_CONTENT)
    


class GetHeathReportByBookingId(APIView):
    def get(self, request, booking_id):
        try:
            booking = Booking.objects.get(booking_id=booking_id)
            
            # Fetching health report data
            health_report = Report.objects.get(booking_id=booking)
            doctor_name = health_report.doctor_id.doctor_name
            patient_name = health_report.patient_id.name
            symptoms = health_report.symptoms
            extra_notes = health_report.extra_notes
            medicine = health_report.medicine
            booking_date=booking.slot.date
            
            # Fetching related test data
            tests = Test.objects.filter(report=health_report)
            
            # Creating a list to store test details
            tests_data = []
            for test in tests:
                test_data = {
                    'test_name': test.test_title.test_name,
                    'test_result': test.result.url,  # Assuming you want the URL to the uploaded file
                    'test_notes': test.notes,
                    'date_of_test': test.date_of_test,
                }
                tests_data.append(test_data)
            
            response_data = {
                'time':booking_date,
                'doctor_name': doctor_name,
                'patient_name': patient_name,
                'symptoms': symptoms,
                'extra_notes': extra_notes,
                'medicine': medicine,
                'tests': tests_data,
            }
            
            return Response(response_data)
        
        except (Booking.DoesNotExist, Report.DoesNotExist):
            return Response({'error': 'No health report found for the given booking ID'})

class TestTitlesListCreateView(ListCreateAPIView):
    queryset=TestTitle.objects.all()
    serializer_class=TestTitleSerializer
    pagination_class = NoPagination 

class TestTitlesRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset=TestTitle.objects.all()
    serializer_class=TestTitleSerializer