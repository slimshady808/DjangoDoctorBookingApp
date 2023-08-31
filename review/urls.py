from django.urls import path
from . import views


urlpatterns = [
    path('', views.getRoutes),
    # path('review-list/',views.get_reviews,name='review-list')
    path('review-list/<int:doctor_id>/',views.ReviewList.as_view(),name='review-list'),
    path('review-list-doc/<int:doctor_id>/',views.ReviewListDoc.as_view(),name='review-list'),
    path('create/',views.CreateReview.as_view(),name='review-create'),
    path('update/<int:review_id>/',views.ReviewUpdate.as_view(),name='review-update')

]