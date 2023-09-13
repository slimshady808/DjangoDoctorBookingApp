from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes),
    # path('register/', views.DoctorRegistrationView.as_view(), name='doctor-register'),
    #path('qualifications/',views.Qualifications.as_view(),name='qualifications'),
    # path('departments/', views.Departments.as_view(), name='departments'),
    path('list/', views.DoctorList.as_view(), name='doctor-profile'),


    path('register/',views.DoctorRegisterationView.as_view(),name="doctor-register"),
#    path('register/',views.register_doctor,name="doctor-register"),


    path('doctors_by_department/<int:department_id>/', views.get_doctors_by_department, name='doctors_by_department'),
    path('doctors/',views.DoctorListView.as_view(),name='doctors-list'),

    path('doctor/<int:pk>/',views.DoctorDetailView.as_view(),name='doctor-detail'),
    
    path('address_edit/<int:pk>/',views.AddressDetailView.as_view(),name='address-detail'),
    path('address_create/',views.AddressCreateView.as_view(),name='address-create'),
    # path('department/<int:department_id>/', views.department_byId, name='department_byId'),
    # path('qualification/<int:qualification_id>/', views.qualification_ById, name='qualification_ById'),
    path('get_available_dates/<int:doctor_id>/', views.get_available_dates, name='get_available_dates'),
    path('get_available_slots/<int:doctor_id>/',views.get_available_slots,name='get_available_slots'),
    path('slot/<int:slotId>/',views.get_date_and_time,name='slot_by_id'),
    path('slot/create/',views.SlotCreateView.as_view(),name='create-slot'),
    path('slot-list/<int:doctor_id>/',views.DoctorAvailableSlotsView.as_view(),name='slot-list'),
    path('slot-delete/<int:slot_id>/',views.SlotDelete.as_view(),name='delete-slot'),
    path('get-doctor-profile/<int:doctor_id>/',views.get_doctor_profile,name='doctor-profile'),
    path('doctor_by_user_id/<int:user_id>/',views.doctor_by_userprofile,name='doctor_by_user_id'),
    
    # Department URLs
    path('departments/', views.DepartmentListCreateView.as_view(), name='department-list-create'),
    path('departments/<int:pk>/', views.DepartmentRetrieveUpdateDeleteView.as_view(), name='department-detail'),

    # Qualification URLs
    path('qualifications/', views.QualificationListCreateView.as_view(), name='qualification-list-create'),
    path('qualifications/<int:pk>/', views.QualificationRetrieveUpdateDeleteView.as_view(), name='qualification-detail'),


]