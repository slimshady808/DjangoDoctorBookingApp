from django.urls import path
from . import views


urlpatterns = [
    path('', views.getRoutes),
    path('create/', views.BookingCreateView.as_view(), name='booking-create'),
    path('pay/', views.start_payment, name="payment"),
    path('payment/success/', views.handle_payment_success, name="payment_success"),
    path('pending-booking/<int:doctor_id>/',views.DoctorPendingPaidBookings.as_view(),name='pending-booking'),
    path('booking-history/<int:doctor_id>/',views.DoctorBookingHistory.as_view(),name='booking_history'),
    path('user-booking-history/',views.UserBookingListView.as_view(),name='user-booking_history')

]