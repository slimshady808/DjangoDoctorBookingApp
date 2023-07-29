from django.urls import path
from . import views
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)
from . views import  MyTokenObtainPairView , RegisterView
# from .views import MyTokenObtainPairView,ForgotPassword,ResetPassword,Listuser,Blockuser,GetProfile,UpdateProfile,ChangePass,ChangeImage

# from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView)

urlpatterns = [
    path('', views.getRoutes),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user-list/', views.userList, name='user-list'),
    path('register', RegisterView.as_view()),
]