from django.urls import path
from . import views
from .views import DoctorListView,DoctorDetailView, AddressDetailView,AddressCreateView

from .views import DoctorRegistrationView, DoctorLoginView, DoctorList,Departments,Qualifications,qualification_ById,department_byId,get_available_slots
urlpatterns = [
    path('', views.getRoutes),
    path('register/', DoctorRegistrationView.as_view(), name='doctor-register'),
    path('login/', DoctorLoginView.as_view(), name='doctor-login'),
    path('list/', DoctorList.as_view(), name='doctor-profile'),
    path('qualifications/',Qualifications.as_view(),name='qualifications'),
    path('departments/', Departments.as_view(), name='departments'),
    path('doctors_by_department/<int:department_id>/', views.get_doctors_by_department, name='doctors_by_department'),
    path('doctors/',DoctorListView.as_view(),name='doctors-list'),
    path('doctor/<int:pk>/',DoctorDetailView.as_view(),name='doctor-detail'),
    path('address_edit/<int:pk>/',AddressDetailView.as_view(),name='address-detail'),
    path('address_create/',AddressCreateView.as_view(),name='address-create'),
    path('department/<int:department_id>/', views.department_byId, name='department_byId'),
    path('qualification/<int:qualification_id>/', views.qualification_ById, name='qualification_ById'),
    path('get_available_dates/<int:doctor_id>/', views.get_available_dates, name='get_available_dates'),
    path('get_available_slots/<int:doctor_id>/',views.get_available_slots,name='get_available_slots'),
     path('refresh/', views.MyTokenRefreshView.as_view(), name='token_refresh'),
    # path('refresh1/', views.refresh_access_token, name='token_refresh'),
    path('slot/<int:slotId>/',views.get_date_and_time,name='slot_by_id'),
    
]