from django.urls import path
from . import views


urlpatterns = [
    path('', views.getRoutes),
    path('create/',views.ReportCreateView.as_view(),name='create_report'),
    path('get-report/<int:booking_id>/',views.ReportRetriveView.as_view(),name='get-report'),
    path('update/<int:report_id>/',views.ReportUpdateView.as_view(),name='update-report'),
    path('test-titles/',views.get_test_titles,name='test-titles'),
    path('test-create/',views.TestReportCreateView.as_view(),name='test-create'),
    path('test-list/<int:report_id>/',views.GetTestsByReportView.as_view(),name='test-list'),
    path('delete/<int:test_id>/',views.DeleteTestView.as_view(),name='delete-test')


]