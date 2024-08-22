from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.LoginApi.as_view(), name='login'),
    path('verify/', views.GetLoginOtp.as_view(), name='verify'),
    path('logout/', views.LogoutView.as_view(), name='LogOut'),

]
