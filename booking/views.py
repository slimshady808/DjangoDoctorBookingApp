from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated 
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView
from rest_framework.generics import ListCreateAPIView
from .models import Booking,Payment
from .serializers import BookingSerializer,PaymentSerializer
from django.shortcuts import get_object_or_404
from django.db.models import F
from doctor.models import Doctor
from account.models import UserProfile,Patient
import json
import jwt
import environ
import razorpay
from django.utils import timezone
from rest_framework.pagination import PageNumberPagination
@api_view(['GET'])
def getRoutes(request):
    routes = [
        'booking/history',
        'booking/create'
    ]
    return Response(routes)

from rest_framework_simplejwt.tokens import RefreshToken

class BookingCreateView(CreateAPIView):

    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    
    def post(self, request, *args, **kwargs):
        # Get the JWT token from the Authorization header
        authorization_header = request.headers.get('Authorization')
        if authorization_header and authorization_header.startswith('Bearer '):
            jwt_token = authorization_header.split(' ')[1]
        else:
            return Response({'error': 'JWT token not provided'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Verify and decode the JWT token
        try:
            decoded_token = RefreshToken(jwt_token, verify=False)
        except Exception as e:
            return Response({'error': 'Invalid JWT token'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Check if the token is expired
        if decoded_token.payload['exp'] < timezone.now().timestamp():
            return Response({'error': 'JWT token has expired'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Print all fields in the JWT token payload
        print("JWT Token Payload:")
        for key, value in decoded_token.payload.items():
            print(f"{key}: {value}")
        
        # Continue with your view logic
        return super().post(request, *args, **kwargs)


env = environ.Env()

environ.Env.read_env()


@api_view(['POST'])
def start_payment(request):
    
    amount = request.data['amount']
    booking_id=request.data['booking']

    if amount is None or booking_id is None :
        return Response({"error":"amount and booking ID are required"},status=400)
    
    try:
        booking_instance =Booking.objects.get(pk=booking_id)
    except Booking.DoesNotExist:
        return Response ({"error":"booking not found"},status=404)
    
    
    # setup razorpay client this is the client to whome user is paying money that's you
    client = razorpay.Client(auth=(env('PUBLIC_KEY'), env('SECRET_KEY')))

    # create razorpay order
    # the amount will come in 'paise' that means if we pass 50 amount will become
    # 0.5 rupees that means 50 paise so we have to convert it in rupees. So, we will 
    # mumtiply it by 100 so it will be 50 rupees.

    payment=client.order.create({"amount":int(amount)*100,
                                 "currency":"INR",
                                 "payment_capture":"1"})
    
    pay=Payment.objects.create(booking=booking_instance,
                               amount=amount,
                               payment_id=payment['id'])
    
    serializer=PaymentSerializer(pay)
    """order response will be 
    {'id': 17, 
    'order_date': '23 January 2021 03:28 PM', 
    'order_product': '**product name from frontend**', 
    'order_amount': '**product amount from frontend**', 
    'order_payment_id': 'order_G3NhfSWWh5UfjQ', # it will be unique everytime
    'isPaid': False}"""

    data={
        "payment":payment,
        "pay":serializer.data
    }

    return Response(data)


@api_view(['POST'])
def handle_payment_success(request):
    # request.data is coming from frontend
    print("Received webhook data:", request.data)
    res = json.loads(request.data["response"])
    print("Webhook response dictionary:", res)
    """res will be:
    {'razorpay_payment_id': 'pay_G3NivgSZLx7I9e', 
    'razorpay_order_id': 'order_G3NhfSWWh5UfjQ', 
    'razorpay_signature': '76b2accbefde6cd2392b5fbf098ebcbd4cb4ef8b78d62aa5cce553b2014993c0'}
    this will come from frontend which we will use to validate and confirm the payment
    """
    ord_id = ""
    raz_pay_id = ""
    raz_signature = ""

    for key in res.keys():
        if key =='razorpay_order_id':
            ord_id = res[key]
        elif key == 'razorpay_payment_id':
            raz_pay_id = res[key]
        elif key == 'razorpay_signature':
            raz_signature = res[key]
        
        # get order by payment_id which we've created earlier with isPaid=False
    print('------>')
   


    print("Looking for payment with payment_id:", ord_id)
        
    pay = Payment.objects.get(payment_id=ord_id)
    print("Found payment:", pay)  

        # we will pass this whole data in razorpay client to verify the payment

    data = {
        'razorpay_order_id': ord_id,
        'razorpay_payment_id': raz_pay_id,
        'razorpay_signature': raz_signature
        }
    print("Verifying payment with data:", data)
    client = razorpay.Client(auth=(env('PUBLIC_KEY'), env('SECRET_KEY')))
        # checking if the transaction is valid or not by passing above data dictionary in 
        # razorpay client if it is "valid" then check will return None
    print("Using Razorpay auth with keys:")
    print("PUBLIC_KEY:", env('PUBLIC_KEY'))
    print("SECRET_KEY:", env('SECRET_KEY'))


    check = client.utility.verify_payment_signature(data)
    print("Payment verification result:", check)
    if check is None:
            print("Redirect to error url or error page")
            return Response({'error': 'Something went wrong'})
        
        # if payment is successful that means check is None then we will turn isPaid=True

    pay.isPaid=True
    pay.save()

    res_data= {
            'message': 'payment successfully received!'
        }
    return Response(res_data)


class DoctorPendingPaidBookings(APIView):
    def get(self, request, doctor_id, format=None):
        try:
            
            user=UserProfile.objects.get(id=doctor_id)
            # Fetch the doctor based on the given doctor_id
            doctor = Doctor.objects.get(user_profile=user)
            
            # Fetch bookings with status 'pending'
            pending_bookings = Booking.objects.filter(doctor=doctor, status='pending')
            
            # Fetch payment ids where isPaid is True
            paid_payment_ids = Booking.objects.filter(payment__isPaid=True).values_list('payment__id', flat=True)
            
            # Filter pending bookings with paid payments
            bookings_with_paid_payments = pending_bookings.filter(payment__id__in=paid_payment_ids)
            
            # Order bookings by slot_date and then by slot_time in ascending order
            ordered_bookings = bookings_with_paid_payments.order_by('slot__date', 'slot__time')
            
            # Prepare data to send in response
            response_data = []
            for booking in ordered_bookings:
                response_data.append({
                    'booking_id': booking.booking_id,
                    'slot_time': booking.slot.time,
                    'slot_date': booking.slot.date,
                    'patient_name': booking.patient_id.name,
                    'doctor_name': booking.doctor.doctor_name,
                    'patient_age': booking.patient_id.age,
                    'patient_id':booking.patient_id.id
                })
            
            return Response(response_data, status=status.HTTP_200_OK)
        
        except Doctor.DoesNotExist:
            return Response({'error': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)

class Doctorid(APIView):
    def get(self, request, doctor_id, format=None):
        user=UserProfile.objects.get(id=doctor_id)
        doctor=Doctor.objects.get(user_profile=user)
        print(doctor.id)
        pending_bookings = Booking.objects.filter(doctor=doctor, status='pending')
        print(pending_bookings)
        return Response({"id":doctor_id})


class DoctorBookingHistory(APIView):
   
    def get(self,request,doctor_id):
        try:
            user=UserProfile.objects.get(id=doctor_id)
            # Fetch the doctor based on the given doctor_id
            doctor = Doctor.objects.get(user_profile=user)

            #bookings for that doctor
            booking=Booking.objects.filter(doctor=doctor)

            # Fetch payment ids where isPaid is True
            paid_payment_ids=Booking.objects.filter(payment__isPaid=True).values_list('payment__id',flat=True)

            #fetch booking with paid payments
            booking_with_paid_payments=booking.filter(payment__id__in=paid_payment_ids)

            #order bookings by slot_date and then by slot_time in ascending order
            ordered_booking=booking_with_paid_payments.order_by('slot__date','slot__time')

            response_data=[]

            for booking in ordered_booking:
                response_data.append({
                    'booking_id':booking.booking_id,
                    'slot_time':booking.slot.time,
                    'slot_date':booking.slot.time,
                    'patient_name':booking.patient_id.name,
                    'patient_age':booking.patient_id.age,
                    'booking_status':booking.status,
                    'patient_id':booking.patient_id.id,
                    'user_id':booking.patient_id.user_profile.id

                })
            return Response(response_data, status=status.HTTP_200_OK)
        except Doctor.DoesNotExist:
            return Response({'error': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)
        


class UserBookingListView(APIView):
    
    def get(self, request,user_id):
        patients=Patient.objects.filter(user_profile=user_id)
        
        user_bookings=Booking.objects.filter(patient_id__in=patients).select_related(
            'doctor','slot','patient'
        ).annotate(
            doctor_name=F('doctor__doctor_name'),
            doctor_image=F('doctor__doctor_image'),
            slot_date=F('slot__date'),
            slot_time=F('slot__time'),
            patient_name=F('patient_id__name'), 
            payment_status=F('status'),
            is_paid=F('payment__isPaid')

        ).values(
            'booking_id', 'doctor_name', 'doctor_image', 'slot_date', 'slot_time', 'patient_name', 'payment_status', 'is_paid'
        ).order_by('-slot_date', 'slot_time') 
        

        return Response({'user_bookings': user_bookings}, status=status.HTTP_200_OK)
         
class AllBookingListView(APIView):
    def get(self,request):

        all_bookings=Booking.objects.all().select_related(
            'doctor','slot','patient'
        ).annotate(
            doctor_name=F('doctor__doctor_name'),
            doctor_image=F('doctor__doctor_image'),
            slot_date=F('slot__date'),
            slot_time=F('slot__time'),
            patient_name=F('patient_id__name'), 
            payment_status=F('status'),
            is_paid=F('payment__isPaid')
        ).values(
            'booking_id', 'doctor_name', 'doctor_image', 'slot_date', 'slot_time', 'patient_name', 'payment_status', 'is_paid'
        ).order_by('-slot_date', 'slot_time')
        
        return Response(all_bookings, status=status.HTTP_200_OK)
