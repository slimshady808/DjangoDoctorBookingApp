from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .models import Review
from .serializers import ReviewSerializer
from rest_framework import status
from rest_framework.generics import CreateAPIView
# Create your views here.


@api_view(['GET'])
def getRoutes(request):
    routes = [
        'review/create',
        'review/update',
        'review/retrieve',
       
    ]
    return Response(routes)

# api_view(['GET'])
# def get_reviews(request):
#     print('comes')
#     try:
#       reviews=Review.objects.all()
#       serializer=ReviewSerializer(reviews,many=True)
#       print(serializer.data)
#       return Response(serializer.data,status=status.HTTP_200_OK)
#     except Review.DoesNotExist:
#        return Response({'error':'review not exist'},status=status.HTTP_404_NOT_FOUND)
class ReviewList(APIView):
    def get(self, request,doctor_id):
        reviews = Review.objects.filter(doctor=doctor_id)
        serializer = ReviewSerializer(reviews, many=True)
       
        return Response(serializer.data)
    
# class ReviewCreate(APIView):
#     def post(self,request,format=None):
#         serializer=ReviewSerializer(data= request.data)
#         if serializer.is_valid():
#             user=request.user
#             doctor_id=serializer.validated_data['doctor']
#             existing_review= Review.objects.filter(user=user,doctor=doctor_id).first()
#             if existing_review:
#                 return Response({'error':'review is already exists'},status=status.HTTP_400_BAD_REQUEST)
#             serializer.save(user=user)
#             return Response(serializer.data,status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
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
    