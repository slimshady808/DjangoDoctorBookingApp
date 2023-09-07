from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .models import Review
from .serializers import ReviewSerializer
from rest_framework import status
from rest_framework.generics import CreateAPIView
from account.models import UserProfile
from doctor.models import Doctor
# Create your views here.


@api_view(['GET'])
def getRoutes(request):
    routes = [
        'review/create',
        'review/update',
        'review/retrieve',
       
    ]
    return Response(routes)


class ReviewList(APIView):
    def get(self, request,doctor_id):
        reviews = Review.objects.filter(doctor=doctor_id)
        serializer = ReviewSerializer(reviews, many=True)
       
        return Response(serializer.data)
    

        
class CreateReview(CreateAPIView):
    queryset=Review.objects.all()
    serializer_class = ReviewSerializer

class ReviewUpdate(APIView):
    def put (self,request,review_id,format=None):
        try:
            review = Review.objects.get(pk=review_id)
        except Review.DoesNotExist:
            return Response({'error':"review not found"},status=status.HTTP_404_NOT_FOUND)
        serializer=ReviewSerializer(review,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response (serializer.data,status=status.HTTP_400_BAD_REQUEST)
 
class ReviewListDoc(APIView):
    def get(self, request,doctor_id):
        user=UserProfile.objects.get(id=doctor_id)
            # Fetch the doctor based on the given doctor_id
        
        doctor = Doctor.objects.get(user_profile=user)
        print(doctor.id)
        reviews = Review.objects.filter(doctor=doctor.id)
        serializer = ReviewSerializer(reviews, many=True)
       
        return Response(serializer.data)

