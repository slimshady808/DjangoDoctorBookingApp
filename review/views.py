from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.decorators import api_view
# Create your views here.


@api_view(['GET'])
def getRoutes(request):
    routes = [
        'review/create',
        'review/update',
        'review/retrieve',
       
    ]
    return Response(routes)

